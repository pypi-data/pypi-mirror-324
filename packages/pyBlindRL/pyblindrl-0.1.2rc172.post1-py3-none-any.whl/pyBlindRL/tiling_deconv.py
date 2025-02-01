from commands import *
import skimage.metrics
import time
import tifffile as tiff
import torch
from cloudvolume import CloudVolume
from tqdm import tqdm
import numpy as np
import os
import shutil
import matplotlib.pyplot as plt


def xy_tiled_image_deconvolution(x, y, z, xy_size, slices, section_size, overlap, blind_iterations, normal_iterations, device, output_dir, trial_name):
    """
    Perform XY Tiled Deconvolution of image with blending
    The outer edge tiles will not be inlucded in the output image

    Parameters:
        x, y, z (int): position upper-left corner of frame on whole image
        xy_size (int): width and height of input image
        slices (int): z depth of image
        section_size (int): size of tiles to calculate on
        overlap (int): amount of pixel overlapping on the edges of tiles for blending
        blind iterations (int): number of blinded iterations to train PSF
        normal iterations (int): number of unblinded iterations performed on each tile
        device (torch device): device tiles are sent to for deconvolution
        output_dir (str): filepath to create trial dir in
        trial_name (str): name of trial
    """

    start_time = time.time()

    #load and setup image from the server
    vol = CloudVolume('precomputed://https://ntracer2.cai-lab.org/data2/051524_bitbow_ch0', parallel=True, progress=True)

    img = vol[x:x+xy_size, y:y+xy_size, z:z+slices]

    img = img [:, :, :, 0]

    img = img.transpose(2, 0, 1)

    deconv_dir = output_dir + "/" + trial_name +  "/deconv"
    imgs_dir = output_dir + "/" + trial_name + "/imgs"

    if not os.path.isdir(output_dir + "/" + trial_name):
        os.mkdir(output_dir + "/" + trial_name)
        os.mkdir(deconv_dir)
        os.mkdir(imgs_dir)

    img_tensor = torch.from_numpy(np.array(img).astype(np.int16))
    psf_guess = np.zeros(np.array(img).shape, dtype=np.complex128)
    psf_piece = generate_initial_psf(np.zeros((slices, section_size, section_size)))

    # make a larger tiled array of PSFs to average later after training
    for i in range(int(xy_size / section_size)):
        for j in range(int(xy_size / section_size)):
            psf_guess[:, (i*section_size):((i+1) * section_size), (j*section_size):((j+1) * section_size)] = psf_piece

    output = torch.clone(img_tensor)

    setup_time = time.time()
    print("Setup Time:")
    print(setup_time - start_time)

    # Blind train an individual PSF for each tile of the original image
    for i in range(int(xy_size / section_size)):
        for j in range(int(xy_size / section_size)):
            for _ in tqdm(range(int(blind_iterations))):

                output_piece, psf_guess_piece, mem = RL_deconv_blind(img_tensor[:, (i*section_size):((i+1) * section_size), (j*section_size):((j+1) * section_size)].type(torch.cdouble), output[:, (i*section_size):((i+1) * section_size), (j*section_size):((j+1) * section_size)].type(torch.cdouble), torch.from_numpy(psf_guess[:, (i*section_size):((i+1) * section_size), (j*section_size):((j+1) * section_size)]).type(torch.cdouble), target_device=device, iterations=1, reg_factor=0)

                output[:, (i*section_size):((i+1) * section_size), (j*section_size):((j+1) * section_size)] = torch.from_numpy(output_piece)
                psf_guess[:, (i*section_size):((i+1) * section_size), (j*section_size):((j+1) * section_size)] = psf_guess_piece

    psf_time = time.time()
    print("Blinded Time")
    print(psf_time - setup_time)

    # Calculate an average PSF from those generated across the entire image
    psf_average = np.zeros((slices, section_size, section_size), dtype=np.complex128)

    for i in range(int(xy_size / section_size)):
        for j in range(int(xy_size / section_size)):
            psf_average[:, :, :] += psf_guess[:, (i*section_size):((i+1) * section_size), (j*section_size):((j+1) * section_size)]

    psf_average = psf_average / ((xy_size / section_size) **2)


    psf_average = unroll_psf(psf_average)
    tiff.imwrite(imgs_dir + "/psf_" + str((1)) + ".tiff", clip_psf(psf_average).astype(np.uint16))

    # Use a larger tile size for the middle of the image
    large_size = section_size + overlap * 2

    psf_average_large = np.zeros((slices, large_size, large_size))
    psf_average_large = emplace_center(psf_average_large, psf_average)
    psf_average_large = roll_psf(psf_average_large)


    average_output = np.zeros((xy_size / section_size,  xy_size/ section_size, slices, large_size, large_size))
    intermediate_output = torch.clone(img_tensor)

    #Deconvolve with the average psf for about as many iterations as the normal image has had itself
    last_tile_idx = (xy_size / section_size) - 1
    for i in range(int(xy_size / section_size)):
        for j in range(int(xy_size / section_size)):

            # If it is in the middle of the image then calculate the deconvolution
            if i > 0 and i < last_tile_idx and j > 0 and j < last_tile_idx:
                output_piece, mem = RL_deconv(img_tensor[:, (i*section_size) - overlap:((i+1) * section_size) + overlap, (j*section_size) - overlap :((j+1) * section_size) + overlap], intermediate_output[:, (i*section_size) - overlap :((i+1) * section_size) + overlap, (j*section_size) - overlap :((j+1) * section_size) + overlap].type(torch.cdouble), torch.from_numpy(psf_average_large).type(torch.cdouble), iterations = normal_iterations, target_device=device)

                average_output[i, j, :, :, :] = output_piece

    average_output = torch.from_numpy(edge_correction(average_output, large_size, section_size, (slices, xy_size, xy_size)))

    normal_deconv_time = time.time()
    print("Normal Deconvolution Time")
    print(normal_deconv_time - psf_time)

    print("PSNR Ratio Score")
    psnr = skimage.metrics.peak_signal_noise_ratio(img_tensor[:, 100:1100, 100:1100].numpy().astype(np.uint16), intensity_match_image(img_tensor[:, 100:1100, 100:1100].numpy().astype(np.uint16), average_output[:, 100:1100, 100:1100].numpy().astype(np.uint16)))
    print(psnr)

    tiff.imwrite(deconv_dir + "/img_" + str((1)) + ".tiff", average_output.numpy().astype(np.uint16))


def z_tiled_image_deconvolution(x, y, z, xy_size, slices, section_size, blind_iterations, normal_iterations, device, output_dir, trial_name, log):
    """
    Perform Z Tiled Deconvolution of image
    Deconvolve the image in stacks in the Z dimension

    Parameters:
        x, y, z (int): position upper-left corner of frame on whole image
        xy_size (int): width and height of input image
        slices (int): z depth of image
        section_size (int): size of tiles to calculate on
        blind iterations (int): number of blinded iterations to train PSF
        normal iterations (int): number of unblinded iterations performed on each tile
        device (torch device): device tiles are sent to for deconvolution
        output_dir (str): filepath to create trial dir in
        trial_name (str): name of trial
        log (bool): save many images during training to log the progression of deconvolution (much much slower)
    """

    start_time = time.time()

    vol = CloudVolume('precomputed://https://ntracer2.cai-lab.org/data2/051524_bitbow_ch0', parallel=True, progress=True)

    img = np.zeros((slices, xy_size, xy_size))

    #cloud volume tends to fail when downloading very large chunks at a time
    #split it up
    for i in range(int(slices/section_size)):
        print(((i * section_size) + z))
        print(((i + 1) * section_size) + z)
        partial_img = vol[x:x+xy_size, y:y+xy_size, ((i * section_size) + z): ((i + 1) * section_size) + z]
        partial_img = partial_img [:, :, :, 0]
        partial_img = partial_img.transpose(2, 0, 1)

        img[(i * section_size):(i + 1) * section_size, :, :] = partial_img

    if os.path.exists(output_dir + "/" + trial_name):
        shutil.rmtree(output_dir + "/" + trial_name)

    os.mkdir(output_dir + "/" + trial_name)

    deconv_dir = output_dir + "/" + trial_name +  "/deconv"
    imgs_dir = output_dir + "/" + trial_name + "/imgs"

    os.mkdir(deconv_dir)
    os.mkdir(imgs_dir)

    img_tensor = torch.from_numpy(np.array(img).astype(np.int16))

    tiff.imwrite(imgs_dir + "/img.tiff", img_tensor.numpy().astype(np.uint16))

    #make the PSF guess just the size of one section and
    #train it blindly on one section of the input image
    psf_guess = generate_initial_psf_smaller(np.zeros((section_size, xy_size, xy_size)), (section_size, section_size, section_size))
    psf_guess = torch.from_numpy(psf_guess)

    output = torch.clone(img_tensor)

    setup_time = time.time()
    print("Setup Time:")
    print(setup_time - start_time)

    blind_mem = 0

    for _ in range(int(1)):
        output_piece, psf_guess_piece, blind_mem = RL_deconv_blind(img_tensor[0:section_size, :, :].type(torch.cdouble), output[0:section_size, :, :].type(torch.cdouble), psf_guess[0:section_size, :, :].type(torch.cdouble), target_device=device, iterations=blind_iterations, reg_factor=0)
        output[0:section_size, :, :] = torch.from_numpy(output_piece)
        psf_guess[0:section_size, :, :] = torch.from_numpy(psf_guess_piece)

    psf_time = time.time()
    print("Blinded Time")
    print(psf_time - setup_time)

    output = torch.clone(img_tensor)

    psnr_values = np.zeros((2, int(normal_iterations/10)))

    normal_mem = 0

    #For the purposes of logging the PSNR properly
    #Iterating on each section iteration by iteration instead of the much more
    #efficent way
    #This way the PSNR can be logged with the same amount of deconvolution across
    #the entire image with the same amount between the sections
    normal_deconv_time = 0
    log_interval = 0
    if log :
        log_interval = 10
    else:
        log_interval = normal_iterations

    for it in tqdm(range(int(normal_iterations/log_interval))):
        for i in range(int(slices / section_size)):
            output_piece, normal_mem = RL_deconv(img_tensor[(i * section_size):((i + 1) * section_size), :, :].type(torch.cdouble), output[(i * section_size):((i + 1) * section_size), :, :].type(torch.cdouble), psf_guess[:, :, :].type(torch.cdouble), iterations = log_interval, target_device=device)
            output[(i * section_size):((i + 1) * section_size), :, :] = torch.from_numpy(output_piece)

        normal_deconv_time = time.time()
        tiff.imwrite(deconv_dir + "/deconv_" + str(((it + 1) * 10)) + ".tiff", output.numpy().astype(np.uint16))
        psnr = skimage.metrics.peak_signal_noise_ratio(img_tensor[:, :, :].numpy().astype(np.uint16), intensity_match_image(img_tensor[:, :, :].numpy().astype(np.uint16), output.numpy().astype(np.uint16)))
        psnr_values[0, int(it)] = (it + 1) * 10
        psnr_values[1, int(it)] = psnr

    print("Normal Deconvolution Time")
    print(normal_deconv_time - psf_time)

    f = open(output_dir + "/" + trial_name + "/data.txt", "w")

    f.write(trial_name)
    f.write("\nLocation: X: " + str(x) + " Y: " + str(y) + " Z: " + str(z))
    f.write("\nRuntime includes logging: " + str(log) + "\n")
    f.write("\nTotal runtime: " + str(time.time() - start_time) + "\n")
    f.write("Blind: Its = " + str(blind_iterations)  + ", Time = " + str(psf_time - setup_time) + ", Memory = " + str(blind_mem / 1e9) + " GB\n")
    f.write("Normal: Its = " + str(normal_iterations) + ", Time = " + str(normal_deconv_time - psf_time) + ", Memory = " + str(normal_mem / 1e9) + " GB\n")
    f.close()

    plt.figure()
    plt.plot(psnr_values[0, :], psnr_values[1, :])

    plt.ylabel("PSNR Score")
    plt.xlabel("Normal Deconvolution Iterations")
    plt.savefig(output_dir + "/" + trial_name + "/psnr.png")
    plt.close()


def h5_input_deconv(section_size, blind_iterations, normal_iterations, device, output_dir, trial_name, log):
    """
    Perform Z Tiled Deconvolution of image that is an h5 input file instead of cloud volume
    Deconvolve the image in stacks in the Z dimension

    Parameters:
        x, y, z (int): position upper-left corner of frame on whole image
        xy_size (int): width and height of input image
        slices (int): z depth of image
        section_size (int): size of tiles to calculate on
        blind iterations (int): number of blinded iterations to train PSF
        normal iterations (int): number of unblinded iterations performed on each tile
        device (torch device): device tiles are sent to for deconvolution
        output_dir (str): filepath to create trial dir in
        trial_name (str): name of trial
        log (bool): save many images during training to log the progression of deconvolution (much much slower)
    """

    import h5py

    start_time = time.time()
    f = h5py.File('/data/jfeggerd/coord_0,0_-23.600,+13.904_ch2.1X.h5', 'r')
    dataset = f['data']

    img = np.array(dataset[:,:,:40])

    img = img.transpose((2, 0, 1))

    xy_size = img.shape[1]
    slices = img.shape[0]

    deconv_dir = output_dir + "/" + trial_name +  "/deconv"
    imgs_dir = output_dir + "/" + trial_name + "/imgs"

    if not os.path.isdir(output_dir + "/" + trial_name):
        os.mkdir(output_dir + "/" + trial_name)
        os.mkdir(deconv_dir)
        os.mkdir(imgs_dir)


    img_tensor = torch.from_numpy(np.array(img).astype(np.int16))

    tiff.imwrite(imgs_dir + "/img.tiff", img_tensor.numpy().astype(np.uint16))

    #make the PSF guess just the size of one section and
    #train it blindly on one section of the input image
    psf_guess = generate_initial_psf_smaller(np.zeros((section_size, xy_size, xy_size)), (section_size, section_size, section_size))
    psf_guess = torch.from_numpy(psf_guess)

    output = torch.clone(img_tensor)

    setup_time = time.time()
    print(torch.cuda.memory_allocated(device))
    print("Setup Time:")
    print(setup_time - start_time)

    blind_mem = 0

    for _ in range(int(1)):
        output_piece, psf_guess_piece, blind_mem = RL_deconv_blind(img_tensor[0:section_size, :, :].type(torch.cdouble), output[0:section_size, :, :].type(torch.cdouble), psf_guess[0:section_size, :, :].type(torch.cdouble), target_device=device, iterations=blind_iterations, reg_factor=0)
        output[0:section_size, :, :] = torch.from_numpy(output_piece)
        psf_guess[0:section_size, :, :] = torch.from_numpy(psf_guess_piece)

    psf_time = time.time()
    print("Blinded Time")
    print(psf_time - setup_time)

    tiff.imwrite(deconv_dir + "/psf" + ".tiff", unroll_psf(psf_guess.numpy().astype(np.uint16)))

    output = torch.clone(img_tensor)

    psnr_values = np.zeros((2, int(normal_iterations/10)))

    normal_mem = 0

    #For the purposes of logging the PSNR properly
    #Iterating on each section iteration by iteration instead of the much more
    #efficent way
    #This way the PSNR can be logged with the same amount of deconvolution across
    #the entire image with the same amount between the sections
    normal_deconv_time = 0
    log_interval = 0
    if log :
        log_interval = 10
    else:
        log_interval = normal_iterations

    for it in tqdm(range(int(normal_iterations/log_interval))):
        for i in range(int(slices / section_size)):
            output_piece, normal_mem = RL_deconv(img_tensor[(i * section_size):((i + 1) * section_size), :, :].type(torch.cdouble), output[(i * section_size):((i + 1) * section_size), :, :].type(torch.cdouble), psf_guess[:, :, :].type(torch.cdouble), iterations = log_interval, target_device=device)
            output[(i * section_size):((i + 1) * section_size), :, :] = torch.from_numpy(output_piece)

        normal_deconv_time = time.time()
        tiff.imwrite(deconv_dir + "/deconv_" + str(((it + 1) * 10)) + ".tiff", output.numpy().astype(np.uint16))
        psnr = skimage.metrics.peak_signal_noise_ratio(img_tensor[:, :, :].numpy().astype(np.uint16), intensity_match_image(img_tensor[:, :, :].numpy().astype(np.uint16), output.numpy().astype(np.uint16)))
        psnr_values[0, int(it)] = (it + 1) * 10
        psnr_values[1, int(it)] = psnr

    print("Normal Deconvolution Time")
    print(normal_deconv_time - psf_time)

    f = open(output_dir + "/" + trial_name + "/data.txt", "w")

    f.write(trial_name)
    # f.write("\nLocation: X: " + str(x) + " Y: " + str(y) + " Z: " + str(z))
    f.write("\nRuntime includes logging: " + str(log) + "\n")
    f.write("\nTotal runtime: " + str(time.time() - start_time) + "\n")
    f.write("Blind: Its = " + str(blind_iterations)  + ", Time = " + str(psf_time - setup_time) + ", Memory = " + str(blind_mem / 1e9) + " GB\n")
    f.write("Normal: Its = " + str(normal_iterations) + ", Time = " + str(normal_deconv_time - psf_time) + ", Memory = " + str(normal_mem / 1e9) + " GB\n")
    f.close()

    plt.figure()
    plt.plot(psnr_values[0, :], psnr_values[1, :])

    plt.ylabel("PSNR Score")
    plt.xlabel("Normal Deconvolution Iterations")
    plt.savefig(output_dir + "/" + trial_name + "/psnr.png")
    plt.close()