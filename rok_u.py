import time

import argparse
from roku import Roku


class RokuWrapper:
    def __init__(self, roku: Roku):
        self.roku = roku

        self.power_on_delay         = 5
        self.basic_command_delay    = 0.1
        self.app_launch_delay       = 8
        self.search_delay           = 2


    def __str__(self):
        return str(self.roku)


    def print_info(self):
        print("[*] Roku info:")
        print("[*]\tIp: {}".format(self.roku.host))
        print("[*]\tDevice info: {}".format(self.roku.device_info))
        print("[*]\tStatus:")
        print("[*]\tPower state: {}".format(self.roku.power_state))

        if self.roku.power_state:
            print("[*]\tActive app: {}".format(self.roku.active_app))


    def power_on(self):
        if not self.roku.power_state:
            self.roku.power()

        time.sleep(self.power_on_delay)


    def power_off(self):
        if self.roku.power_state:
            self.roku.power()


    def select(self):
        self.roku.select()
        time.sleep(self.basic_command_delay)


    def up(self):
        self.roku.up()
        time.sleep(self.basic_command_delay)


    def down(self):
        self.roku.down()
        time.sleep(self.basic_command_delay)


    def right(self):
        self.roku.right()
        time.sleep(self.basic_command_delay)


    def left(self):
        self.roku.left()
        time.sleep(self.basic_command_delay)


    def launch(self, app_name):
        app = self.roku[app_name]
        if app is None:
            raise(Exception("{} not found".format(app_name)))

        app.launch()

        time.sleep(self.app_launch_delay)


    def play_youtube_video(self, title, creepy_text=False):
        try:
            self.launch("YouTube")
        except Exception as e:
            print("[-] Failed to launch YouTube: {}".format(e))
            return

        # Usually first thing on the screen is an error message
        # due to launching YouTube from python api, select to ignore this
        self.select()

        # Takes a second to process exiting error message
        time.sleep(1)

        # Go left to left dashboard
        self.left()

        # Up to search
        self.up()

        # Right into search interface
        self.right()

        # Go down and hover clear button
        self.right()
        self.down()
        self.down()
        self.down()
        self.down()
        self.right()

        if creepy_text:
            self.roku.literal("I'm watching you")

            # Time for them to read it
            time.sleep(2)
            # Clear text
            self.select()

            self.roku.literal("You know...")

            # Time for them to read it
            time.sleep(1)
            # Clear text
            self.select()

            self.roku.literal("I used to live here")

            # Time for them to read it
            time.sleep(1)
            # Clear text
            self.select()

        # Write the title of the video into search interface
        self.roku.literal(title)

        # Sleep a little to make sure the literal is fully written into seach
        # (there is also slight delay because YouTube tries to load some videos
        # with from the given text
        time.sleep(1)

        # Click search button
        self.right()
        self.select()

        # Delay as YouTube actually loads search results
        time.sleep(2)

        # Select first search result
        self.select()


    def list_apps(self):
        print("[*] Available apps:")
        for app in self.roku.apps:
            print("[*]\t{}".format(app.name))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-r", "--roku-ip",
                    type=str,
                    help="Roku IP address to use (will discover if not present)")
    ap.add_argument("-d", "--delay",
                    type=int,
                    help="Add a delay after device is selected")
    ap.add_argument("-c",
                    "--creepy-text",
                    action="store_true",
                    help="Add in creepy text before video plays")

    vid_args = ap.add_mutually_exclusive_group(required=True)
    vid_args.add_argument("--suggest-videos",
                          action="store_true",
                          help="List some funny youtube videos to play")
    vid_args.add_argument("-i", "--video_index", type=int, help="Index of video from --sugest-videos")
    vid_args.add_argument("-v", "--video_title", type=str, help="Video title to play")

    args = ap.parse_args()

    favorite_videos = ["[ASMR] Whispering 750+ Names",
                       "Monster Inc. Theme (EARRAPE)",
                       "Creepy Weeping Ghost Sound Effect",
                       "Creepy Little Girl Talking, Singing"]

    if args.suggest_videos:
        for i in range(len(favorite_videos)):
            print("{}: {}".format(i, favorite_videos[i]))
        return

    if args.video_index >= len(favorite_videos):
        print("[-] Video index must be one of the videos from --sugest-videos")
        return

    if args.roku_ip:
        roku = Roku(args.roku_ip)
    else:
        devices = Roku.discover(timeout=3)

        if len(devices) == 0:
            print ("[*] No roku devices found")
            return

        elif len(devices) == 1:
            roku = devices[0]
            print("[+] Found roku: {}".format(roku))
        else:
            print("Multiple roku devices found:")
            for i in range(len(devices)):
                print("{}: {}".format(i, devices[i]))

            selection = input("Please select from the listed rokus\n")

            try:
                selection = int(selection)

                roku = devices[selection]
            except ValueError as e:
                print("[-] Selection must be an integer")
                return
            except Exception as e:
                print("[-] Selection must be one of the listed devices")
                return

            print("[*] Device selected: {}".format(roku))

    roku_wrapped = RokuWrapper(roku)

    roku_wrapped.print_info()
    print("[*]")
    roku_wrapped.list_apps()

    return

    if args.delay:
        time.sleep(args.delay)

    roku_wrapped.power_on()

    if args.video_index:
        roku_wrapped.play_youtube_video(favorite_videos[args.video_index],
                                        creepy_text=args.creepy_text)
    elif args.video_title:
        roku_wrapped.play_youtube_video(args.video_title,
                                        creepy_text=args.creepy_text)

    #roku_wrapped.play_youtube_video("[ASMR] Whispering 750+ Names", creepy_text=True)
    #roku_wrapped.play_youtube_video("Monster Inc. Theme (EARRAPE)")
    #roku_wrapped.play_youtube_video("Creepy Weeping Ghost Sound Effect", creepy_text=True)
    #roku_wrapped.play_youtube_video("Creepy Little Girl Talking, Singing", creepy_text=True)

    return


if __name__ == "__main__":
    main()
