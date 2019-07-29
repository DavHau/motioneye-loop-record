### Script to enable loop recording on motion / motioneye / motionEyeOs or any other Surveillance system
#### Motivation:
When setting up motionEyeOs on a raspberry pi zero recently, i noticed that motionEyeOs lacks a functionality called 'Loop Recoding', a common mechanism for surveillance systems that prevents the storage from running full by deleting the oldest recordings whenever free space gets scarce. There is a 'delete footage after X days' functionality, but since the amount of footage recorded within a specific time is depending on how frequent motion is detected, there is no guarantee that the storage will not run full even when using this setting.
I know that there are open feature requests for adding loop recording on [motioneyeos](https://github.com/ccrisan/motioneyeos), but since this is not done yet, i wrote this little addon script that adds the Loop Recoding functionality to your motionEyeOs. Though motionEyeOs is not required to run this script and it could also be used for any other surveillance system.

Please feel free to contribute your ideas or improvements.

#### How it works
After installation, a script will check the free space of the filesystem each time a recording is saved. If the free space is under a certain threshold, it will start deleting files, beginning with the oldest one until the configured threshold is reached again.

#### Usage without motionEyeOs
The script itself does not contain any motion(Eye) specific code and can be used on all kinds of systems which are able to run python. Just execute the loop_delete.py periodically (via cron for example).

##### Usage:
```bash
usage: loop_delete.py [-h] --dir DIR --space MEGABYTES
```
To delete as many old files from DIR until MEGABYTES of space is available

#### Installation on MotionEyeOs
Once installed, the addon becomes a part of the configuration and therefore will be backed up and restored by motionEye's backup/restore functionality.

Login to your motionEye web interface as admin and enable SSH under 'Services', save and wait for the device to reboot.
Then login to your device via SSH with your admin user and password which you normally use for logging in to the web interface:

###### Step 1: login via SSH
Linux:
```bash
ssh admin_username@ip_address_of_motioneyeos
```

Windows:

Use Putty to login to your motionEyeOs via ssh. HowTo's on how to use Putty can be found on the internet, like [this](https://mediatemple.net/community/products/dv/204404604/using-ssh-in-putty-) for example.

###### Step 2: Install the Addon script
After being logged in successfully, a commandline terminal will open. Copy the following command into the terminal and hit Enter. This will install the addon.
```bash
curl https://raw.githubusercontent.com/DavHau/motioneye-loop-record/master/loop_delete.py > /data/etc/loop_delete.py && chmod +x /data/etc/loop_delete.py
```

###### Step 3: Enable the addon in the web iterface
- Use your browser to login to the web interface of your MotionEyeOs.
- Open the Settings and go to 'File Storage'.
- Turn on 'Run A Command'. A text field will appear to enter a command.
- Copy the following command into the text field, but replace '/data/output' in case you use a different root directory for your recodings.
```
/data/etc/loop_delete.py -d /data/output/ -s 500
```
This will always ensure that at least 500 MB will be kept free in /data/output/.

You can of course change the threshold of 500 to your needs.
