import argparse
from multiprocessing import Pool
import soundfile
from glob import glob
from tqdm import tqdm
import os


def check_files(audio_file_path):
    audio_info = soundfile.info(audio_file_path)
    status_flag = 0

    if audio_info.samplerate != 8000:
        status_flag = 1
    if audio_info.channels != 1:
        status_flag = 2
    if audio_info.subtype != "PCM_16":
        status_flag = 3
    if audio_info.format != "WAV":
        status_flag = 4

    return status_flag, os.path.realpath(audio_file_path)


def main(audio_file_paths: list, num_job: int) -> None:
    results = {0: set(), 1: set(), 2: set(), 3: set(), 4: set()}

    with Pool(processes=num_job) as pool:
        for _ in tqdm(
            pool.imap(check_files, audio_file_paths), total=len(audio_file_paths)
        ):
            k, v = _
            results[k].add(v)

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("audio_dir")
    parser.add_argument("--nj", dest="num_job", type=int, default=100)
    parser.add_argument("--print_valid", dest="print_valid", action="store_true")
    parser.add_argument("--print_invalid", dest="print_invalid", action="store_true")

    args = parser.parse_args()

    audio_file_paths = glob(f"{args.audio_dir}/**/*.wav", recursive=True)
    results = main(audio_file_paths, args.num_job)

    print(f"valid: {len(results[0])} files")
    print(f"invalid: {sum(len(results[_]) for _ in range(1,5))} files")
    print(f"  sample rate error: {len(results[1])} files")
    print(f"  channel error: {len(results[2])} files")
    print(f"  sub type error: {len(results[3])} files")
    print(f"  format error: {len(results[4])} files")

    if args.print_valid:
        for _ in results[0]:
            print(_)

    if args.print_invalid:
        for i in range(1, 5):
            for _ in results[i]:
                print(_)
