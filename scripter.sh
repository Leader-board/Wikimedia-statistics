#!/bin/bash
echo "$@"
cd /statdata/Wikimedia-statistics
for((i=1;i<=$#;i++)); 
do mysql --defaults-file="$HOME"/replica.my.cnf -h "${!i}".analytics.db.svc.wikimedia.cloud "${!i}"_p -e "SELECT user_name, user_registration, user_editcount from user ORDER BY user_editcount desc;" > "${!i}".csv;
done
rm -r ../rawcsv
mkdir -p ../rawcsv
mv *.csv ../rawcsv
rm -r ../processed_csv
mkdir -p ../processed_csv
export MAVEN_OPTS="-Xmx29000m"
cd "Global user table generator"
time mvn compile exec:java -Dexec.mainClass="Main"
time python3 "pushtowiki.py"
time python3 "user_data.py"
