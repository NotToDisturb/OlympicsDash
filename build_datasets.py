from dataset_generators.base_dataset import BaseDataset
from dataset_generators.medals_dataset import MedalsDataset
from dataset_generators.gender_dataset import GenderDataset
from dataset_generators.top_5_sports_dataset import Top5SportsDataset

if __name__ == "__main__":
    build_datasets = [MedalsDataset, GenderDataset, Top5SportsDataset]
    for dataset in build_datasets:
        print(f"[INFO] Building dataset '{dataset.get_name()}'")
        dataset.build_dataset()
    print("[SUCCESS] All datasets built")
