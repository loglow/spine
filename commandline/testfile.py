import crawler
import spider

BAD_FILES = [
    "enkidu_rot.blend", "gilgamesh_eyebrows.blend", "gilgamesh_sim.blend",
    "a1s01_link_actions_a3s20.blend", "a1s02.blend", "a1s02gravel.blend",
    "a1s02light.blend", "a2s00.blend", "a2s49.blend", "a2s49light.blend",
    "track_old.blend", "tracks.blend", "train.blend", "train_merge1.blend",
    "roach_smash.blend", "ad.blend", "train-nizu.blend"]

PATH = "/home/bassam/old/bassam/projects/hamp/tube"

def crawl():
    svn = spider.ProjectTree(PATH)
    files = (f for f in svn.all_files() if all(b not in f for b in BAD_FILES))
    tube = crawler.ProjectCrawler(PATH)
    tube.clear()
    tube.check_files(files)
    tube.save()

if __name__ == "__main__":
    crawl()
