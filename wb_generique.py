from flask import Flask, jsonify, make_response, Response, request
import requests, json

import mysql.connector as m
from datetime import datetime
from flask_httpauth import HTTPTokenAuth
import hashlib
import re
import socket
import ssl
from operator import itemgetter
from functions import *
from pathlib import Path

import _md5
import hashlib
#from os import scandir
import os

import functions
import random
#import plibt smt
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import string
from datetime import datetime
from datetime import timedelta
#from src.utils import get_project_root
app = Flask(__name__)

@app.route('/get_collab', methods=['GET'])
# @token_auth.login_required
def get_collab():
    try:
        print(request.args.get('mail'))
        print(request.args.get('api_key'))
        print(request.args.get('collab'))
        cnx=m.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)
        if request.args.get('mail') != None:
            if (autorization(request.args.get('api_key'), request.args.get('mail'), None)) == False:
                return jsonify("session_error"), 401
            else:
                collab = request.args.get('collab')
                sql = ('SELECT * from users left join adresses on users.location = adresses.id left join villes on adresses.ville = villes.id where MD5(users.id) = %s ')
                cur = cnx.cursor()
                cur.execute(sql, (collab,))
                rv = cur.fetchall()
                cnx.commit()
                cur.close()
                print(rv)
                l = []
                for e in rv:
                    l.append({'id': e[0], 'nom': e[1], 'prenom': e[2], 'mail': e[5]})

                return jsonify(l), 200
    except:
        cnx = m.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)
        if l:
            return jsonify(l), 201
        else:
            return jsonify({'message': 'collab introuvable!!'}), 200
#*******************************************************************************************************************************************************************

@app.route('/get_collab_qualif', methods=['GET'])
# @token_auth.login_required
def get_collab_qualif():
    try:
        print(request.args.get('mail'))
        print(request.args.get('api_key'))
        print(request.args.get('id'))
        cnx=m.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)
        if request.args.get('mail') != None:
            if (autorization(request.args.get('api_key'), request.args.get('mail'), None)) == False:
                return jsonify("error 0792"), 401
            else:
                id = request.args.get('id')
                print(id)
                sql = "select users.id,users.nom,users.prenom,users.code from qualif_collab_aff left join users on qualif_collab_aff.id_collab = users.id where md5(qualif_collab_aff.id_qualif) = %s and users.active  = 1"
                cur = cnx.cursor()
                cur.execute(sql, (id,))
                rv = cur.fetchall()
                cnx.commit()
                cur.close()
                print('le resultat4=', rv)
                l = []
                for e in rv:
                    l.append({'id': e[0], 'nom': e[1], 'prenom': e[2], 'code': e[3]})

                return jsonify(l), 200

    except:
        cnx = m.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)
        if l:
            return jsonify(l), 201
        else:
            return jsonify({'message': 'id introuvable!!'}), 200
#*******************************************************************************************************************************************************************
@app.route('/all_users_active', methods=['GET'])
# @token_auth.login_required
def all_users_active():
    try:
        print(request.args.get('mail'))
        print(request.args.get('api_key'))
        cnx=m.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)
        if request.args.get('mail') != None:
            if (autorization(request.args.get('api_key'), request.args.get('mail'), None)) == False:
                return jsonify("error 0792"), 401
            else:
                sql = "SELECT md5(id) as id,nom,prenom FROM users where active= 1"
                cur = cnx.cursor()
                cur.execute(sql)
                rv = cur.fetchall()
                print(rv)
                cnx.commit()
                cur.close()
                l = []
                for e in rv:
                    l.append({'id': e[0], 'nom': e[1], 'prenom': e[2]})

                return jsonify(l), 200
    except:
        cnx = m.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)
        if rv:
            return jsonify(l), 201
        else:
            return jsonify({'message': 'aucun utilisateur active!'}), 200
#*******************************************************************************************************************************************************************
@app.route('/all_group_users_active', methods=['GET'])
# @token_auth.login_required
def all_group_users_active():
    try:
        print(request.args.get('mail'))
        print(request.args.get('api_key'))
        cnx=m.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)
        if request.args.get('mail') != None:
            if (autorization(request.args.get('api_key'), request.args.get('mail'), None)) == False:
                return jsonify("error 0792"), 401
            else:
                sql = "SELECT md5(groupe_collab.id) AS id, groupe_collab.nom AS groupe FROM groupe_collab LEFT JOIN groupe_user ON groupe_user.id_groupe = groupe_collab.id LEFT JOIN users ON users.id = groupe_user.id_users WHERE users.active = 1 GROUP BY groupe_collab.nom"
                cur = cnx.cursor()
                cur.execute(sql)
                rv = cur.fetchall()
                print(rv)
                cnx.commit()
                cur.close()
                l = []
                for e in rv:
                    l.append({'id': e[0], 'group': e[1]})

                return jsonify(l), 200
    except:
        cnx = m.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)
        if rv:
            return jsonify(l), 201
        else:
            return jsonify({'message': 'aucun groupe active!'}), 200

#*******************************************************************************************************************************************************************
@app.route('/add_commentaire_opportunite', methods=['GET'])
# @token_auth.login_required
def add_commentaire_opportunite():
    try:
        result=''
        response ={}
        cnx = m.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019', database='interface',
                        port=1433)
        if request.args.get('mail') != None:
            if (autorization(request.args.get('api_key'), request.args.get('mail'), None)) == False:
                return jsonify("session_error"), 401
            else:
                print('autorisation')
                print(request.args.get('mail'))
                print(request.args.get('api_key'))
                print(request.args.get('id_user'))
                print(request.args.get('comment'))
                print(request.args.get('id_opp'))
                print(request.args.get('idpros'))
                id_user = request.args.get('id_user')
                row_user = get_all_user_id(id_user)
                id_user = row_user[0]
                print('id_user',id_user)
                comment = request.args.get('comment')
                print('comment',comment)
                id_opp = request.args.get('id_opp')
                id_opp1 = get_id_opp(id_opp,cnx)
                id_opp=id_opp1[0][0]
                print('id_opp',id_opp)
                idpros = request.args.get('idpros')
                idpros=get_idpros_md5(idpros,cnx)[0][0]
                print('idpros',idpros)

                #comment = str.replace("'", " ", comment)
                #comment = str.replace('"', " ", comment)
                print(comment)
                style=''
                print(cnx)
                id_service =get_service_opp(id_opp,cnx)[0][0]
                print('id_service',id_service)
                if (id_service == 1) :
                    style = "rgba(27, 186, 225, 0)"
                elif (id_service == 2) :
                    style = "rgba(27, 186, 225, 0.2)"
                elif (id_service == 3):
                    style = "rgba(27, 186, 225, 0.4)"
                elif (id_service == 4) :
                    style = "rgba(27, 186, 225, 0.6)"
                elif (id_service == 5) :
                    style = "rgba(27, 186, 225, 0.8)"
                print('style',style)
                print(cnx)

                print('add')
                rv = get_commentaire_opportunite(id_opp, id_user, comment, style, cnx)
                print('rv', rv)
                if rv:
                    result = rv
                else:
                    sql = "INSERT INTO commentaire_opportunite set  opp=%s , user=%s ,commentaire=%s, style=%s "
                    cur = cnx.cursor()
                    cur.execute(sql, (id_opp, id_user, comment, style,))
                    rv = get_commentaire_opportunite(id_opp, id_user, comment, style, cnx)
                    print('rv', rv)
                    result=rv
                    cnx.commit()
                    cur.close()


                print('result',result)

                commentaire_action = "Modifications fiche sans changement de statut"
                print(comment)
                action = Addaction(id_opp,id_user,None,idpros,commentaire_action,comment,cnx)
                print(action)
                if result!='':
                    response['error']=False
                    response['id']=result
                else:
                    response['error'] = True

                return jsonify(response), 200
    except:
        cnx = m.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019', database='interface',port=1433)
        if response:
            return jsonify(response), 200
        else:
            return jsonify({'error': True}), 201
#*******************************************************************************************************************************************************************
@app.route('/add_commentaire_prospect', methods=['GET'])
# @token_auth.login_required
def add_commentaire_prospect():
    try:
        response =''
        cnx=m.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)
        if request.args.get('mail') != None:
            if (autorization(request.args.get('api_key'), request.args.get('mail'), None)) == False:
                return jsonify("session_error"), 401
            else:
                print('autorisation')
                print(request.args.get('mail'))
                print(request.args.get('api_key'))
                print(request.args.get('id_user'))
                print(request.args.get('comment'))
                print(request.args.get('id_prospect'))
                id_prospect = request.args.get('id_prospect')
                id_user = request.args.get('id_user')
                print('id_user',id_user)
                comm = request.args.get('comment')
                style ="rgba(27, 186, 225, 0)"
                print('pas')
                rv = get_commentaire_prospect(id_prospect, id_user, comm, style, cnx)
                print('rv')
                print(rv)
                if rv :
                    response='La ligne existe déjà'
                else:
                    sql = ('INSERT INTO commentaire_prospect set  id_prospect= %s , user= %s ,commentaire= %s , style= %s')
                    cur = cnx.cursor()
                    cur.execute(sql, (id_prospect,id_user,comm,style,))
                    #cur.execute(sql,(str(id_prospect),str(id_user),str(comm),str(style),))
                    #rv = cur.fetchall()
                    #print('rv',rv)
                    rv=get_commentaire_prospect(id_prospect,id_user,comm,style,cnx)
                    print('rv')
                    print(rv)
                    cnx.commit()
                    cur.close()
                    if rv:
                        response = 'ligne ajoutée avec succès'
                    else:
                        response ='erreur d ajout'


                return jsonify({'message': response}), 200
    except:
        cnx = m.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)
        if response:
            return jsonify({'message': response}), 201
        else:
            return jsonify({'message': 'ERREUR!!'}), 200


#*******************************************************************************************************************************************************************
@app.route('/list_document_contrat', methods=['GET'])
# @token_auth.login_required
def list_document_contrat():
    #try:
    response = []
    print(request.args.get('mail'))
    print(request.args.get('api_key'))
    cnx = m.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019', database='interface', port=1433)
    if request.args.get('mail') != None:
        if (autorization(request.args.get('api_key'), request.args.get('mail'), None)) == False:
            return jsonify("error 0792"), 401
        else:
            print('autorisation')

            id = request.args.get('id_contrat')
            print(id)
            id_affaire = request.args.get('id_affaire')
            origin_path = request.args.get('origin_path')
            id_contrat = get_id_contrat_md5(id, cnx)[0][0]
            print(id_contrat)

            result = list_document(id, cnx)
            print('list_doc', result)
            e=None

            for e in result:
                print(e)
                document = e
                tmp = {}
                tmp['id'] = hashlib.md5(str(document[0]).encode('utf-8')).hexdigest()
                tmp['libelle'] = document[1]
                tmp['signature'] = document[4]
                tmp['form'] = document[3]
                tmp['oblig'] = document[5]
                tmp['list_files'] = {}
                print('tmp=',tmp)

                # str(os.environ['DOCUMENT_ROOT'])
                path = "_SERVER['DOCUMENT_ROOT']" + origin_path +str(id_contrat) + "/" + str(id_affaire) + "/s_" + str(document[0]) + "/"
                if os.path.isdir(path):
                    files = os.scandir(path)
                    if files:
                        while e in files:
                            if ('.' != e and '..' != e):
                                tmp1 = {}
                                tmp1['name'] = e
                                tmp1['size'] = e.stat().st_size
                                tmp1['path'] = origin_path + id_contrat + "/" + id_affaire + "/s_" + document[0] + "/" + e
                            tmp['list_files'] = tmp1
                            response.append(tmp)

            return jsonify(response), 200

    '''except:
        cnx = m.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',
                        database='interface', port=1433)
        if response:
            return jsonify(response), 201
        else:
            return jsonify({'message': 'Erreur!'}), 200'''

#*******************************************************************************************************************************************************************
@app.route('/load_list_document', methods=['GET'])
# @token_auth.login_required
def load_list_document():
    try:
        response=[]
        print(request.args.get('mail'))
        print(request.args.get('api_key'))
        cnx=m.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)
        if request.args.get('mail') != None:
            if (autorization(request.args.get('api_key'), request.args.get('mail'), None)) == False:
                return jsonify("error 0792"), 401
            else:
                print('autorisation')
                id_contrat = request.args.get('id_contrat')
                id_contrat = get_id_contrat_md5(id_contrat,cnx)[0][0]
                print(id_contrat)
                id_document=request.args.get('id_document')
                print(id_document)
                id_document=get_id_document_md5(id_document,cnx)[0][0]
                print(id_document)
                id_affaire = request.args.get('id_affaire')
                id_affaire = get_id_affaire_md5(id_affaire,cnx)[0][0]
                print(id_affaire)
                #print(os.environ['DOCUMENT_ROOT'])
                #str(os.environ['DOCUMENT_ROOT'])+
                #root = get_project_root()
                #str(os.environ.get('document_root','document_root'))
                print(os.environ)

                for a in os.environ:
                    print( a,'::', os.getenv(a))
                path1 =str(os.environ.get('',''))+"/src/documents/"+str(id_contrat)+"/"+str(id_affaire)+"/s_"+str(id_document)+"/"
                print('path')
                print(path1)
                print(os.path.isdir(path1))
                if Path.is_dir(path1):
                    files = os.scandir(path1)
                    if files:
                        for file in files :
                            if ('.' != file and '..' != file) :
                                tmp ={}
                                tmp['name'] = file
                                tmp['size'] = file.stat().st_size
                                tmp['path'] = "/src/documents/"+id_contrat+"/"+id_affaire+"/s_"+id_document+"/"+file
                                print(tmp)
                                response.append(tmp)


                return jsonify(response), 200
    except:
        cnx = m.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)
        if response:
            return jsonify(response), 201
        else:
            return jsonify({'message': 'Erreur!'}), 200

#*******************************************************************************************************************************************************************
@app.route('/get_hist_opp', methods=['GET'])
# @token_auth.login_required
def get_hist_opp():
    try:
        response = []
        print(request.args.get('mail'))
        print(request.args.get('api_key'))
        cnx = m.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019', database='interface', port=1433)
        if request.args.get('mail') != None:
            if (autorization(request.args.get('api_key'), request.args.get('mail'), None)) == False:
                return jsonify("session_error"), 401
            else:
                print('autorisation')
                id_opp = request.args.get('id')
                origin_path = request.args.get('origin_path')
                id_opp = get_id_opp(id_opp,cnx)[0][0]
                print(id_opp)
                print(cnx)
                res_list_hist = hist_opp(id_opp,cnx)
                print(res_list_hist)
            for row in res_list_hist:
                print(row)
                tmp = {}
                tmp['icon'] = row[12]
                tmp['color'] = row[13]
                if (row[12] ==None):
                    tmp['icon'] = "fa-certificate"
                    tmp['color'] = "#000000"
                tmp['user'] = row[7]
                tmp['commentaire'] = row[5]
                tmp['description'] = row[10]
                tmp['date'] = row[6]
                print(tmp['date'])
                print(row[0])
                res_file_action = get_file_action("id_action_opp",row[0],cnx)
                print(res_file_action)
                tmp['file'] = ""
                for row_file in res_file_action :
                    if row_file[4] == 1:
                        tmp['file']+= row_file[1]
                    else:
                        #DOMAIN_HOST+
                        tmp['file'] += 'http://149.202.243.51:5000/'+origin_path+id_opp+"/"+row_file[1]
                response.append(tmp)
        return jsonify(response), 200
    except:
        cnx = m.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019', database='interface', port=1433)
        if response:
            return jsonify(response), 201
        else:
            return jsonify({'message': 'Erreur!'}), 200
#*******************************************************************************************************************************************************************
@app.route('/get_list_ville', methods=['GET'])
# @token_auth.login_required
def get_list_ville():
    try:
        '''print(request.args.get('mail'))
        print(request.args.get('api_key'))
        print(request.args.get('cp'))'''
        cnx=m.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)
        if request.args.get('mail') != None:
            if (autorization(request.args.get('api_key'), request.args.get('mail'), None)) == False:
                return jsonify("error 0792"), 401
            else:
                cp = request.args.get('cp')
                sql = "SELECT id, nom_comm from villes where postal_code= %s "
                cur = cnx.cursor()
                cur.execute(sql, (cp,))
                rv = cur.fetchall()
                cnx.commit()
                cur.close()
                l = []
                for e in rv:
                    l.append({'idVille': e[0], 'Ville': e[1]})
                return jsonify(l), 200
    except:
        cnx = m.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)
    if l != []:
            return jsonify(l), 200
    else:
            return jsonify({'message': 'Code postal introuvable'}), 201

#********************************************************************************************************************************************************************


@app.route('/get_all_event_negocia', methods=['GET'])
# @token_auth.login_required
def get_all_event_negocia():
    try:
        response = []
        cnx=m.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)
        if request.args.get('mail') != None:
            if (autorization(request.args.get('api_key'), request.args.get('mail'), None)) == False:
                return jsonify("error 0792"), 401
            else:
                collaborateur = request.args.get('collaborateur')
                print(collaborateur)
                start =request.args.get('start')
                print(start)
                end = request.args.get('end')
                print(end)
                r1=list_category_user(collaborateur,cnx)
                print('r1=',r1)
                str1 = ','.join(r1[0])
                cat = str1.split('|')
                print('cat=',cat)
                print('len',len(cat))
                k=0
                s=0
                tmp = {}
                rdv=None

                while k<len(cat):
                    categorie = cat[k]
                    print('categorie,k',categorie,k)
                    id_cat =categorie[0:1]
                    rdv=getallopportunite_event_negoci(collaborateur, start, end,id_cat,cnx)
                    cnx.commit()
                    print('rdv',rdv)
                    j=0
                    if rdv != []:
                        s=k
                        '''for e in rdv[0]:#(j<len(rdv[0])):
                            print(j,':',e)
                            j+=1'''
                        i=0
                        print('************************************************************')
                        while i<len(rdv):
                            tmp["editable"]=False
                            tmp['icon'] = '<i class="fa'+rdv[i][3]+'">'
                            tmp["id"] = "opp_"+str(rdv[i][4])
                            tmp["start"] = rdv[i][9]
                            tmp["end"] = rdv[i][10]
                            tmp['etat'] = rdv[i][5]
                            tmp['color'] = rdv[i][43]
                            tmp['textColor'] = rdv[i][2]
                            tmp['title'] = rdv[i][46]+' '+rdv[i][51]
                            print('tmp=',tmp)
                            icon_int=''
                            '''if (rdv[i][26] != None & rdv[i][26] != ""):
                                icon_int = '<img src="img/icon_int1.png" />'''
                            i += 1
                            if i==len(rdv):
                                break
                        time_start =(tmp["start"])
                        time_end = (tmp["end"])
                        if time_end <= time_start:
                            time_start=+(timedelta(minutes=30))
                            #tmp["end"] = time_start.tzinfo('Y-m-d H:i:s')

                        tmp['details'] = '<br>'+str(rdv[s][46])+str(rdv[s][47])+' '+icon_int+'</b><br>Type : '+str(rdv[s][0])+'<br>Tél : '+ str(rdv[s][48])+'<br>Mobile : '+ str(rdv[s][49])+'<br>Campagne : '+ str(rdv[s][52])+'<br>Heure début : '+ str(rdv[s][9])+"<br>statut : "+ str(rdv[s][5])+' <br>Adresse : '+ str(rdv[s][53])+' '+ str(rdv[s][54])+' '+ str(rdv[s][55])+' '+ str(rdv[s][50])+' '+ str(rdv[s][51])
                        tmp['url'] = 'DOMAIN_HOST'+'/editer_rdv_suivi.php?rdv='+str(rdv[s][4])+'&tous=true'
                        response.append(tmp)

                        result_not = getall_not(collaborateur, start, end,cnx)
                        print("result_not",result_not)

                        e=0
                        print('************************************************************')
                        while e < len(result_not):
                            nott =result_not[e]
                            tmp = {}
                            tmp['editable'] = False
                            if ( nott[9] == 'info') :
                                tmp['color'] = "#b2cce5"
                            elif ( nott[9] == 'danger'):
                                tmp['color'] = "#FF0000"
                            elif ( nott[9] == 'warning'):
                                tmp['color'] = "#FFA500"
                            tmp['icon'] = '<i class="fa fa-dashboard"></i>'
                            #time = datetime.datetime.strptime(nott[8], "%m/%d/%Y")
                            #print('time=',time)
                            #endTime = datetime("H:i:s", datetime.datetime.strptime('+30 minutes', time))
                            tmp["id"] = 'not_'+ str(nott[0])
                            tmp["start"] =  str(nott[7])+' '+ str(nott[8])
                            tmp["end"] =(nott[7])+(nott[8])+timedelta(minutes=30)#endTime
                            tmp['title'] =  nott[0]
                            tmp['details'] =  str(nott[2])+"<br>Date : "+ str(nott[7])+ "<br>Heure : "+ str(nott[8])
                            tmp['url'] = "DOMAIN_HOST"+"/editer_not.php?id="+hashlib.md5(str(nott[0]).encode('utf-8')).hexdigest()
                            print('tmp_not=',tmp)
                            response.append(tmp)
                            e+=1
                            if e==len(result_not):
                                print('fin_not')
                                break
                        print('************************************************************')

                        result_event = getall_event(collaborateur, start, end, cnx)
                        print("result_event", result_event)

                        if result_event:
                            e=0
                            while e <len(result_event):
                                event =result_event[e]
                                tmp={}
                                tmp['editable'] = True
                                tmp['icon'] = '<i class="fa fa-child"></i>'
                                tmp["id"] = 'event_'+str(event[0])
                                tmp["start"] = event[2]
                                tmp["end"] = event[3]
                                tmp['color'] = "#C0C0C0"
                                tmp['title'] = event[1]
                                tmp['details'] = str(event[1])+"<br>Date début : "+str(event[2])+"<br>Date fin  : "+str(event[3])
                                print('tmp_event=',tmp)
                                response.append(tmp)
                                e += 1
                                if e == len(result_not):
                                    print('fin_event')
                                    break
                            print('************************************************************')

                    k += 1
                    if k == len(cat):
                            print('fin_all_event_negocia')
                            break

    except:
        cnx = m.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)
    if response:
            return jsonify(response), 200
    else:
            return jsonify({'message': 'ERREUR!'}), 201


#*******************************************************************************************************************************************************************


'''
@app.route('/select_user_mail', methods=['GET'])
# @token_auth.login_required
def select_user_mail():
    while True:
        try:
            cur = cnx.cursor()
            mail = request.args.get('mail')
            sql = "SELECT id_session,date_update_pass FROM users WHERE mail= %s "
            cur.execute(sql, (str(mail),))
            rv = cur.fetchall()
            cur.close()
            if rv != []:
                for e in rv:
                    id = e[0]
                    date = e[1]
                    dateUp = datetime.strptime(str(date), "%Y-%m-%d")
                    maintenant = datetime.now()
                    ecartSecondes = (maintenant - dateUp).days

                return jsonify({'nombre de jour': ecartSecondes, 'id session': id}), 200

            else:
                return jsonify({'message': 'Adresse introuvable'}), 201
            break
        except:
            cnx = mariadb.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',
                                  database='interface', port=1433)'''
#*******************************************************************************************************************************************************************

if __name__=="__main__":
   #app.run(host='149.202.243.51',port=5000,debug=True)
   app.run(debug=True)