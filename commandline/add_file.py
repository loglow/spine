import spider
import crawler
import sys
import os

BAD_FILES = [
    "gilgamesh_eyebrows.blend", "enkidu_rot.blend",
    "gilgamesh_sim.blend", "ad.blend", "roach_smash.blend", "track_old.blend",
    "tracks.blend", "train-nizu.blend", "train.blend", "train_merge1.blend",
    "a1s02.blend", "a1s01_link_actions_a3s20.blend","a1s02gravel.blend",
    "a1s02light.blend", "a2s00.blend", "a2s49.blend", "a2s49light.blend",
    "a3s30crowd.blend", "meshcasher.blend", "group_override_scene.blend",
    "gilgalight_uplight.blend", "gilgalight_backlight.blend", "gilgalight.blend",
    "dustlocal.blend", "scenes/dev/"]
PATH = "/home/bassam/projects/hamp/tube"
DEV = "/home/bassam/projects/hamp/tube/scenes/dev"

def add_file():
    tube = crawler.ProjectCrawler(PATH)
    tube.check_file(sys.argv[-1])
    tube.save()
    print("SAVED")

def crawl_dev():
    tube = crawler.ProjectCrawler(PATH)
    files = [f for f in os.listdir(DEV) if f.endswith('.blend')]
    for f in files:
        tube.check_file(os.path.join("scenes/dev/", f))
        tube.save()
        print("SAVED", f)


if __name__ == "__main__":
    #crawl_dev()
    add_file()
