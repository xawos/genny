# Genny

I chose this name because it's a cute image generator running on cute hardware.

It's a simple Python script that randomizes parameters and generates images.

It also adds metadata information such as prompt used, time taken for each step and the IP+hostname that generated it.

After generation it moves the image to another folder (NFS in my case) and starts with a new one.

The `sd` file contains an example run of the script with the original prompt, along with 2 example durations (the [RISCV](https://milkv.io/docs/duo/getting-started/duos) takes ~12 hours for a full image, a rpi2w ~1h)

I'm too lazy to create the `requirements.txt`, go ahead and try :)

The folders are there just as an example, `magicfile` is a quick and dirty way to check if NFS is mounted, change the path for those two and it should work.

Maybe I'll add a webpage in the future to show those images, for now it simply generates them.

###### Code is mostly self-explanatory, if you have any doubt ask an LLM :)

## Credits 
- [Random_prompt](https://github.com/GaelicThunder/custom-stable-diffusion-raspberry/blob/main/random_prompt.py)

- [OnnxStream](https://github.com/vitoplantamura/OnnxStream), especially Vito's help in [this issue](https://github.com/vitoplantamura/OnnxStream/issues/91), couldn't run it on RISCV without his help (and project) ❤️

- [get_ip](https://stackoverflow.com/a/28950776/3549452)
