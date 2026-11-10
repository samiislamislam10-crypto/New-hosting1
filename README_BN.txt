JISAN X SAMI - PREMIUM TCP HOSTING
Termux Python Flask panel

নতুন ফিচার:
- Admin Panel-এর Default Files Folder-এ একসাথে অনেকগুলো .py ফাইল Upload করা যাবে
- Default Files Folder-এ রাখা সব .py ফাইল নতুন User Registration করলে তার নিজের private folder-এ কপি হবে
- প্রতিটি User-এর ফাইল আলাদা থাকবে; অন্য User-এর ফাইল দেখা বা পরিবর্তন করা যাবে না
- Admin default file Remove করলে শুধু মূল template মুছবে; আগের User-দের কপি থাকবে
- Bright neon colour, gradient এবং smooth animation UI

অন্যান্য ফিচার:
- Multi-user register/login
- Password hash
- Python .py upload, view, delete
- main.py-তে শুধু Uid ও Pw পরিবর্তনের আলাদা editor; অন্য কোড edit করা যায় না
- প্রতি user-এর একটি করে script process
- Start / Stop / Restart
- Console log
- Admin user list/delete
- Mobile responsive SAMI YT branding

DEFAULT FILES যোগ করার নিয়ম:
1) Admin account দিয়ে Login করো
2) Admin Panel খোলো
3) Default Files Folder অংশে এক বা একাধিক .py file select করো
4) Add Default Files চাপো
5) এরপর নতুন User Register করলে সব Default .py file তার Dashboard-এর File Manager-এ চলে যাবে

গুরুত্বপূর্ণ:
- নতুন Default File যোগ করলে তা পরবর্তী নতুন User-দের কপি হবে। আগে থেকে থাকা User-দের ফাইলে নিজে থেকে যোগ হবে না।
- একই নামের Default File আগে থাকলে নতুন Upload skip হবে। আগে পুরোনোটি Remove করে তারপর নতুনটি Upload করো।
- Upload করা Python script panel চালানো একই Android/Termux account-এর অধিকার পায়। তাই অচেনা user-কে account দেবে না এবং public internet-এ সরাসরি expose করবে না। এটি OS-level sandbox নয়, production-grade shared hosting-ও নয়।
- ডিফল্টে শুধু 127.0.0.1-এ চলে। VPS-এ চালালে HTTPS, firewall এবং OS-level per-user/container isolation দরকার।

INSTALL (Termux):
1) pkg update && pkg upgrade -y
2) pkg install python unzip -y
3) ZIP extract করে project folder-এ ঢোকো
4) pip install -r requirements.txt
5) প্রথম admin password environment দিয়ে সেট করো:
   export PANEL_ADMIN_USER=admin
   export PANEL_ADMIN_PASSWORD='একটি শক্তিশালী পাসওয়ার্ড'
   export PANEL_SECRET="$(python -c 'import secrets; print(secrets.token_hex(32))')"
6) python app.py
7) Android browser-এ খোলো:
   http://127.0.0.1:5000

প্রথমবার DB তৈরি হলে admin account তৈরি হবে। পরে environment password বদলালেও আগের account password বদলাবে না।
ডিফল্ট Admin ID: admin
ডিফল্ট Admin Password: ChangeMe123!
প্রথম Login-এর পর Password পরিবর্তন করে নিও।
Admin panel: /admin
User register: /register
