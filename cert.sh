echo -n $'[1] Generate Certificate\n[2] Renew Certificate\n>'
read opt

if [ $opt == 1 ] ; then
	sudo sudo certbot certonly --standalone --preferred-challenges http -d aspys.tk
	sudo certbot --nginx
elif [ $opt == 2 ] ; then
	sudo certbot renew
fi
