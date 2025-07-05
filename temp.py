import os
import yaml

class FolderAndMdMaker:
    """폴더 및 2단계(최종) md 파일 생성"""
    def __init__(self, yaml_data, base_dir):
        self.data = yaml_data
        self.base_dir = base_dir

    def make_folders_and_mds(self):
        for item in self.data['content']:
            for key, value in item.items():
                folder = key
                for sub in value.get('sub', []):
                    for sub_key, sub_value in sub.items():
                        sub_path = os.path.join(self.base_dir, folder, sub_key)
                        os.makedirs(sub_path, exist_ok=True)
                        md_path = os.path.join(sub_path, f"{sub_key}.md")
                        with open(md_path, 'w', encoding='utf-8') as f:
                            f.write(f"# {sub_value.get('title', sub_key)}\n")

class IndexMaker:
    """index.md 생성 (상위 폴더별로 분류, 2단계 md로 바로 링크)"""
    def __init__(self, yaml_data, base_dir):
        self.data = yaml_data
        self.base_dir = base_dir

    def make_index(self):
        index_path = os.path.join(self.base_dir, "index.md")
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write("# Index\n\n")
            for item in self.data['content']:
                for key, value in item.items():
                    folder = key
                    folder_title = value.get('title', folder)
                    f.write(f"## {folder_title}\n\n")
                    for sub in value.get('sub', []):
                        for sub_key, sub_value in sub.items():
                            sub_title = sub_value.get('title', sub_key)
                            sub_md = os.path.join(folder, sub_key, f"{sub_key}.md")
                            f.write(f"- [{sub_title}]({sub_md})\n")
                    f.write("\n")

class SeriesLinker:
    """YAML의 sub 항목만 참조하여, 각 2단계 폴더의 md 파일에 같은 그룹 내 다른 md 파일 링크 추가"""
    def __init__(self, yaml_data, base_dir):
        self.data = yaml_data
        self.base_dir = base_dir

    def link_series(self):
        for item in self.data['content']:
            for key, value in item.items():
                folder = key
                for sub in value.get('sub', []):
                    for sub_key, sub_value in sub.items():
                        subfolder_path = os.path.join(self.base_dir, folder, sub_key)
                        md_filename = f"{sub_key}.md"
                        md_path = os.path.join(subfolder_path, md_filename)
                        # 해당 폴더 내의 모든 파일 중 폴더명.md를 제외한 파일만 추출
                        other_files = [
                            f for f in os.listdir(subfolder_path)
                            if f != md_filename and os.path.isfile(os.path.join(subfolder_path, f))
                        ]
                        if other_files:
                            with open(md_path, 'a', encoding='utf-8') as f:
                                f.write("\n## 목록\n\n")
                                for other in other_files:
                                    f.write(f"- [{other}](./{other})\n")

class Page(FolderAndMdMaker, IndexMaker, SeriesLinker):
    def __init__(self, yaml_path):
        with open(yaml_path, 'r', encoding='utf-8') as f:
            yaml_data = f.read()
        data = yaml.safe_load(yaml_data)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        FolderAndMdMaker.__init__(self, data, base_dir)
        IndexMaker.__init__(self, data, base_dir)
        SeriesLinker.__init__(self, data, base_dir)
        self.make_folders_and_mds()
        self.make_index()
        self.link_series()

# 사용 예시:
if __name__ == "__main__":
    yaml_path = r"C:\Users\parkj\Documents\workspace\my_projects\7_project\my_page\organizer.yml"
    Page(yaml_path)