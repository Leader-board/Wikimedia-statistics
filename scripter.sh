for((i=1;i<=$#;i++)); 
do mysql --defaults-file=$HOME/replica.my.cnf -h ${!i}.analytics.db.svc.wikimedia.cloud ${!i}_p -e "SELECT user_name, user_registration, user_editcount from user;" > ${!i}.csv; 
done
