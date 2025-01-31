#!/usr/bin/bash
# set -x  # show command for debug
PASSWD='wo9aifree$om'
PORT=18962
HOST='xinlin@114.215.183.12'
ADDR="$HOST -p $PORT"
TMPFILE='_TT01'
export AUTOPASS=$PASSWD


# check if python is available
# use which and echo $?


echo '* test ssh remote single command with -p'
python autopass.py -p $PASSWD ssh $ADDR 'ls -hl'

echo '* test ssh remote single command with env AUTOPASS'
python autopass.py ssh $ADDR 'pwd'

echo '* test ssh remote multi-command'
python autopass.py ssh $ADDR 'echo 1;echo 2;echo 3;'

echo '* test ssh remote bash builtin cmd'
python autopass.py ssh $ADDR 'type type'

echo '* test ssh remote pipeline |'
python autopass.py ssh $ADDR 'ls -hl | grep repos'

echo '* test ssh local pipeline |'
python autopass.py ssh $ADDR 'ls -lh' | grep repos

echo '* test scp a file to remote then ssh bash'
echo 'date' >  $TMPFILE
echo 'date' >> $TMPFILE
echo 'date' >> $TMPFILE
echo 'date' >> $TMPFILE
python autopass.py scp -P $PORT $TMPFILE $HOST:~/
python autopass.py ssh $ADDR "bash $TMPFILE"
python autopass.py ssh $ADDR "rm $TMPFILE;echo 'rm done'"
rm $TMPFILE

echo '* test scp a big file'
dd if=/dev/zero of=./$TMPFILE bs=4096 count=20480 status=progress  # 80M
python autopass.py scp -P $PORT $TMPFILE $HOST:~/
python autopass.py ssh $ADDR "rm $TMPFILE;echo 'rm done'"
rm $TMPFILE

echo '* test redirect, there is a ssh warning'
echo 'echo 1;date;date;date;echo 2' > $TMPFILE
python autopass.py -t15 -p $PASSWD ssh $ADDR < $TMPFILE
rm $TMPFILE


echo '* test sudo local command'
echo 'Hi, there...' > $TMPFILE
python autopass.py -t5 -p $PASSWD sudo cat $TMPFILE  # no double quote here
python autopass.py -p $PASSWD sudo cat $TMPFILE  # no double quote here
python autopass.py -p $PASSWD sudo cat $TMPFILE  # no double quote here
rm $TMPFILE



