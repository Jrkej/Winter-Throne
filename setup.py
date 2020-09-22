import os
import psycopg2
import datetime
from flask import Flask, render_template,request,redirect,url_for
import json
import requests
import sqlite3 as sql

bot_programming = "fantastic-bits"
DATABASE_URL = os.environ['DATABASE_URL']
app = Flask(__name__)
info = []
first = []
final = []

def bot_programming_getter():
    a=["fantastic-bits","tulips-and-daisies","a-code-of-ice-and-fire"]
    winner=[0,0,0]
    votes=retrievevote()
    for v in votes:
        v=v[0]
        for b in range(len(a)):
            if v == a[b]:
                vo=b
        winner[vo] += 1
    print(winner)
    m=-1
    for c in range(len(winner)):
        b=winner[c]
        if b > m:
            m=b
            ret=a[c]
    return ret

def check_time(tn):
    date = 22
    month = 9
    hour = 5
    minute = 0
    date_today = int(tn.strftime("%d"))
    month_now = int(tn.strftime("%m"))
    hour_now = int(tn.strftime("%H"))
    minute_now = int(tn.strftime("%M"))
    date+=month*30
    hour+=date*24
    minute+=hour*60
    date_today+=month_now*30
    hour_now+=date_today*24
    minute_now+=hour_now*60
    if minute <= minute_now:
        return True
    return False

def check_end_time(tn):
    date = 22
    month = 9
    hour = 5
    minute = 15
    date_today = int(tn.strftime("%d"))
    month_now = int(tn.strftime("%m"))
    hour_now = int(tn.strftime("%H"))
    minute_now = int(tn.strftime("%M"))
    date+=month*30
    hour+=date*24
    minute+=hour*60
    date_today+=month_now*30
    hour_now+=date_today*24
    minute_now+=hour_now*60
    if minute <= minute_now:
        return True
    return False

def check_re_time(tn):
    date = 22
    month = 9
    hour = 5
    minute = 10
    date_today = int(tn.strftime("%d"))
    month_now = int(tn.strftime("%m"))
    hour_now = int(tn.strftime("%H"))
    minute_now = int(tn.strftime("%M"))
    date+=month*30
    hour+=date*24
    minute+=hour*60
    date_today+=month_now*30
    hour_now+=date_today*24
    minute_now+=hour_now*60
    if minute <= minute_now:
        return True
    return False

def get_rankings(bot):
    Leaderboard=[]
    leagues = ["legend","gold","silver","bronze","wood1","wood2","wood3"]
    for name in leagues:
        try:
            cg = requests.post('https://www.codingame.com/services/Leaderboards/getFilteredPuzzleLeaderboard',json = [bot,"c96627d7b482084183f526c125ae497b","global",{"active":True,"column":"LEAGUE","filter":name}]) 
            Leaderboard.extend(cg.json()['users'])
            print(name,len(cg.json()['users']))
        except:
            pass
    return Leaderboard

def str_leaderboard():
    bot_programming=bot_programming_getter()
    leda=get_rankings(bot_programming)
    a=""
    for i in leda:
        try:
            a+=str(i['pseudo'])+"|"+str(i['rank'])+" "
        except:
            pass
    a=a[:-1]
    return a

def update_first():
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur=con.cursor()
    l=str_leaderboard()
    sqlite_insert_with_param = f"UPDATE initial_rank SET leaderboard = '{l}' WHERE id = 'a';"
    cur.execute(sqlite_insert_with_param)
    con.commit()

def update_final(save):
    a=""
    for i in save:
        for k in i:
            a+=str(k)+"|"
        a=a[:-1]
        a+=" "
    a=a[:-1]
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur=con.cursor()
    sqlite_insert_with_param=f"UPDATE final_rank SET leaderboard = '{a}' WHERE id='a';"
    cur.execute(sqlite_insert_with_param)
    con.commit()

def createfirstleaderboard():
    print("creating table")
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur=con.cursor()
    cur.execute("CREATE TABLE initial_rank(id TEXT,leaderboard TEXT)")
    print("created table")
    con.commit()
    cur=con.cursor()
    l=str_leaderboard()
    sqlite_insert_with_param = f"INSERT INTO initial_rank(id,leaderboard) VALUES ('a','{l}');"
    cur.execute(sqlite_insert_with_param)
    con.commit()

def createfinalleaderboard():
    print("creating table")
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur=con.cursor()
    cur.execute("CREATE TABLE final_rank(id TEXT,leaderboard TEXT)")
    con.commit()
    print("created table")
    cur=con.cursor()
    sqlite_insert_with_param = f"INSERT INTO final_rank(id,leaderboard) VALUES ('a','a');"
    cur.execute(sqlite_insert_with_param)
    con.commit()

def get_final():
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur=con.cursor()
    cur.execute("SELECT leaderboard FROM final_rank")
    a=cur.fetchall()
    a=a[0]
    a=a[0]
    s=a.split()
    print("splited")
    r=[]
    for i in s:
        r.append([i.split("|")])
    return r

def createvoterlist():
    print("creating table")
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur=con.cursor()
    table="""
        CREATE TABLE vote (
            name TEXT
        )
        """
    cur.execute(table)
    con.commit()
    print("created table")

def insertvote(vote):
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = con.cursor()
    sqlite_insert_with_param = f"INSERT INTO vote(name) VALUES ('{vote}');"
    cur.execute(sqlite_insert_with_param)
    con.commit()
    con.close()

def retrievevote():
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = con.cursor()
    cur.execute("SELECT name FROM vote")
    users = cur.fetchall()
    con.close()
    return users

def createtable():
    print("creating table")
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur=con.cursor()
    table="""
        CREATE TABLE Participa (
            name TEXT
        )
        """
    cur.execute(table)
    con.commit()
    print("created table")

def insertUser(nam):
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = con.cursor()
    sqlite_insert_with_param = f"INSERT INTO Participa(name) VALUES ('{nam}');"
    print(sqlite_insert_with_param)
    cur.execute(sqlite_insert_with_param)
    con.commit()
    con.close()

def retrieveUsers():
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = con.cursor()
    cur.execute("SELECT name FROM Participa")
    users = cur.fetchall()
    con.close()
    return users

def initial_rank(user,curr_leaderboard):
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = con.cursor()
    cur.execute("SELECT leaderboard FROM initan_rank")
    l = cur.fetchall()
    con.close()
    l=l.split()
    for p in l:
        p=p.split("|")
        if p[0] == user:
            return int(p[1])
    return len(curr_leaderboard)

def scrape_data(part):
    global info
    participants=[]
    for n in part:
        participants.append(n[0])
    info=[]
    data=[]
    leagueFinder = {0:'wood 2', 1:'wood 1', 2:'bronze', 3:'silver', 4:'gold', 5:'legend'}
    bot_programming=bot_programming_getter()
    print(bot_programming)
    if bot_programming == "a-code-of-ice-and-fire":
        leagueFinder = {0:'wood 3', 1:'wood 2', 2:'wood 1', 3:'bronze', 4:'silver', 5:'gold',6:'legend'}
    leaderboard=get_rankings(bot_programming)
    if check_time(datetime.datetime.now()) == False:
        update_first()
    for cgdata in leaderboard:
        try:
            if cgdata['pseudo'] in participants:
                username = cgdata['pseudo']
                cgrank = cgdata['rank']
                lerank = cgdata['localRank']
                points = cgdata['score']
                league = leagueFinder[cgdata['league']['divisionIndex']]
                player = cgdata['codingamer']
                country = player['countryId']
                language = cgdata['programmingLanguage']
                sub="No"
                progress = cgdata['percentage']
                if progress != 100:
                    sub="yes"
                rank_progress=initial_rank(cgdata['pseudo'],leaderboard)-cgrank
                data.append([username,cgrank,lerank,points,league,language,country,sub,progress,rank_progress])
        except:
            continue
        data.sort(key = lambda a:a[1])
    for p in range(len(data)):
        info.append([p+1,data[p][0],data[p][1],data[p][2],data[p][3],data[p][4],data[p][5],data[p][6],data[p][7],data[p][8],data[p][9]])
    if check_end_time(datetime.datetime.now()) == False:
        update_final(info)
    else:
        info=get_final()

@app.route("/")
def main():
    try:
        createtable()
    except:
        print("table is already there")
    try:
        createvoterlist()
    except:
        print("voter list is there")
    try:
        createfirstleaderboard()
    except:
        print("Leaderboard table is there")
    try:
        createfinalleaderboard()
    except:
        print("Final leaderboard table is already there")
    return redirect(url_for("home"))

@app.route("/home",methods=["GET","POST"])
def home():
    if request.method == "GET":
        return render_template("home.html")
    else:
        log = request.form['sub']
        if log == "Register":
            return redirect(url_for("registeration"))
        else:
            return redirect(url_for("leaderboard"))

@app.route("/registeration",methods=["GET","POST"])
def registeration():
    if request.method == "GET":
        return render_template("register.html",voting=check_time(datetime.datetime.now()))
    else:
        if check_re_time(datetime.datetime.now()):
            return render_template("Error.html",code="You are late registration closed....")
        name = request.form['id']
        try:
            vote = request.form['vote']
        except:
            pass
        try:
            all_p=retrieveUsers()
            new=True
            for p in all_p:
                if p[0] == name:
                    new=False
                    break
            if new:
                insertUser(name)
                try:
                    insertvote(vote)
                    print(vote)
                except:
                    pass
            else:
                return render_template("Error.html",code=f"{name} already registered....")
            return redirect(url_for("leaderboard"))
        except Exception as e:
            return render_template("Error.html",code=f"{name} can't register retry... error = {e}")

@app.route("/leaderboard")
def leaderboard():
    try:
        part=retrieveUsers()
        scrape_data(part)
        bo=bot_programming_getter()
        msg=f"The Contest is About {bo}"
        p=len(set(part))
        end=""
        if check_end_time(datetime.datetime.now()):
            end=".Contest Ended."
        print(check_time(datetime.datetime.now()))
        print(check_end_time(datetime.datetime.now()))
        if check_time(datetime.datetime.now()) == False:
            msg="Bot programming is a suspense.."
            return render_template("leaderboard.html",message="Total registered players = "+str(p),msg=msg)
        return render_template("leaderboard.html",players = info,message="Total registered players = "+str(p)+end,msg=msg)
    except Exception as e:
        return render_template("Error.html",code=f"Error in retrieving users or taking data from CG,error = {e}")

@app.route("/data")
def data():
    try:
        part=retrieveUsers()
        print(part)
        votes=retrievevote()
        print(votes)
        return render_template("leaderboard.html",players = part)
    except:
        return render_template("Error.html",code="1")

@app.route("/before_leaderboard")
def before_leaderboard():
    try:
        part=retrieveUsers()
        scrape_data(part)
        bo=bot_programming_getter()
        msg=f"The Contest is About {bo}"
        return render_template("leaderboard.html",players = info,msg=msg,message=str(datetime.datetime.now()))
    except:
        return render_template("Error.html",code="Error in retrieving users or taking data from CG")

if __name__ == "__main__":
    app.run()
