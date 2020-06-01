import binascii

responses = {}

responses["mounts"] = '''/dev/root / ext4 rw,noatime 0 0
devtmpfs /dev devtmpfs rw,relatime,size=469544k,nr_inodes=117386,mode=755 0 0
sysfs /sys sysfs rw,nosuid,nodev,noexec,relatime 0 0
proc /proc proc rw,relatime 0 0
tmpfs /dev/shm tmpfs rw,nosuid,nodev 0 0
devpts /dev/pts devpts rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=000 0 0
tmpfs /run tmpfs rw,nosuid,nodev,mode=755 0 0
tmpfs /run/lock tmpfs rw,nosuid,nodev,noexec,relatime,size=5120k 0 0
tmpfs /sys/fs/cgroup tmpfs ro,nosuid,nodev,noexec,mode=755 0 0
cgroup2 /sys/fs/cgroup/unified cgroup2 rw,nosuid,nodev,noexec,relatime,nsdelegate 0 0
cgroup /sys/fs/cgroup/systemd cgroup rw,nosuid,nodev,noexec,relatime,xattr,name=systemd 0 0
cgroup /sys/fs/cgroup/cpu,cpuacct cgroup rw,nosuid,nodev,noexec,relatime,cpu,cpuacct 0 0
cgroup /sys/fs/cgroup/cpuset cgroup rw,nosuid,nodev,noexec,relatime,cpuset 0 0
cgroup /sys/fs/cgroup/devices cgroup rw,nosuid,nodev,noexec,relatime,devices 0 0
cgroup /sys/fs/cgroup/freezer cgroup rw,nosuid,nodev,noexec,relatime,freezer 0 0
cgroup /sys/fs/cgroup/memory cgroup rw,nosuid,nodev,noexec,relatime,memory 0 0
cgroup /sys/fs/cgroup/net_cls cgroup rw,nosuid,nodev,noexec,relatime,net_cls 0 0
cgroup /sys/fs/cgroup/pids cgroup rw,nosuid,nodev,noexec,relatime,pids 0 0
cgroup /sys/fs/cgroup/blkio cgroup rw,nosuid,nodev,noexec,relatime,blkio 0 0
'''

responses["dd"] = binascii.unhexlify("7f454c46 01 02 01 00 0000000000000000 0002 0008 00000001 00404da0 00000034 00000000 50001005 00340020 00080000 00000000".replace(" ", ""))

responses["tftp"] = '''BusyBox v1.31.0 (2019-07-16 01:13:11 UTC) multi-call binary.

Usage: tftp [OPTIONS] HOST [PORT]

Transfer a file from/to tftp server

	-l FILE	Local FILE
	-r FILE	Remote FILE
	-g	Get file
	-p	Put file
	-b SIZE	Transfer blocks of SIZE octets
'''

responses["wget"] = '''BusyBox v1.31.0 (2019-07-16 01:13:11 UTC) multi-call binary.

Usage: wget [-c|--continue] [--spider] [-q|--quiet] [-O|--output-document FILE]
	[-o|--output-file FILE] [--header 'header: value'] [-Y|--proxy on/off]
	[-P DIR] [-S|--server-response] [-U|--user-agent AGENT] [-T SEC] URL...

Retrieve files via HTTP or FTP

	--spider	Only check URL existence: $? is 0 if exists
	-c		Continue retrieval of aborted transfer
	-q		Quiet
	-P DIR		Save to DIR (default .)
	-S    		Show server response
	-T SEC		Network read timeout is SEC seconds
	-O FILE		Save to FILE ('-' for stdout)
	-o FILE		Log messages to FILE
	-U STR		Use STR for User-Agent header
	-Y on/off	Use proxy
'''
