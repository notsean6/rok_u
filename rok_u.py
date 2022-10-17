from roku import Roku


def play_youtube_video(roku, title):
        youtube = roku['YouTube']
        if youtube is None:
            print("[-] Youtube not found")
            return

        youtube.launch()

        import time
        time.sleep(8)

        roku.select()
        time.sleep(0.5)
        roku.left()
        time.sleep(0.5)
        roku.up()
        time.sleep(0.5)
        roku.right()
        time.sleep(0.5)
        roku.literal(title)
        time.sleep(2)
        time.sleep(0.1)
        roku.right()
        time.sleep(0.1)
        roku.down()
        time.sleep(0.1)
        roku.down()
        time.sleep(0.1)
        roku.down()
        time.sleep(0.1)
        roku.down()
        time.sleep(0.1)
        roku.right()
        time.sleep(0.1)
        roku.right()
        time.sleep(0.1)
        roku.select()
        time.sleep(2)
        roku.select()


def main():
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

        print("[*] Status:")
        print("[*] Power state: {}".format(roku.power_state))

        if roku.power_state:
            print("[*] Active app: {}".format(roku.active_app))

        print("[*] Available apps:")
        for app in roku.apps:
            print(app.name)

        print(dir(roku))

        #play_youtube_video(roku, "[ASMR] Whispering 750+ Names")
        play_youtube_video(roku, "Monster Inc. Theme (EARRAPE)")

        return


if __name__ == "__main__":
    main()
