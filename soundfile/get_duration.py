import argparse
from multiprocessing import Pool
import soundfile
from glob import glob
from tqdm import tqdm


def get_duration(audio_file_path: str) -> float:
    try:
        return soundfile.info(audio_file_path).duration
    except:
        return 0.0


def main(audio_file_paths: list, num_job: int) -> None:
    duration = 0.0
    with Pool(processes=num_job) as pool:
        for _ in tqdm(
            pool.imap(get_duration, audio_file_paths), total=len(audio_file_paths)
        ):
            duration += _

    print(f"{len(audio_file_paths)} files")
    print(f"{round(duration, 2)} seconds")
    print(f"{round(duration / 3600, 2)} hours")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("audio_dir")
    parser.add_argument("--nj", dest="num_job", type=int, default=100)

    args = parser.parse_args()

    audio_file_paths = glob(f"{args.audio_dir}/**/*.wav", recursive=True)
    main(audio_file_paths, args.num_job)
