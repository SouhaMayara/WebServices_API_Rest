import os
from typing import Any, Union

import mysql.connector
from datetime import datetime
from flask_httpauth import HTTPTokenAuth
import hashlib
import mysql.connector as mariadb
from flask import Flask, jsonify, make_response, Response, request, make_response
import requests, json



def get_commentaire_prospect(id_prospect,id_user,comm,style,cnx):
    print('fonction')
    cursor = cnx.cursor()
    print(cursor)
    rowcount = ('SELECT * FROM commentaire_prospect WHERE id_prospect= %s AND user= %s AND commentaire= %s AND style= %s')
    cursor.execute(rowcount,(id_prospect,id_user,comm,style,))
    print(cursor)
    actions = cursor.fetchall()
    cursor.close()
    print('actions=', actions)
    if actions:
        return True
    else:
        return False
#*********************************************************************************************************************************
def get_id_opp(id,cnx):
    cursor = cnx.cursor()
    rowcount = ('SELECT id from opportunite where md5(id) = %s')
    cursor.execute(rowcount, (id,))
    actions = cursor.fetchall()
    cursor.close()
    print('actions=', actions)
    return actions



def hist_opp(id_opp,cnx):
    print('get_hist_opp')
    cursor = cnx.cursor()
    rowcount = ('SELECT * FROM action where opp = %s')
    cursor.execute(rowcount, (id_opp,))
    actions = cursor.fetchall()
    cursor.close()
    print('actions=', actions)
    return actions
#*********************************************************************************************************************************
def get_service_opp(id_opp,cnx):
    print('get_service_opp')
    cursor = cnx.cursor()
    rowcount = ('SELECT etat_opp.categorie FROM etat_opp LEFT JOIN opportunite ON etat_opp.id = opportunite.etat_rdv_id WHERE opportunite.id =%s ')
    cursor.execute(rowcount, (id_opp,))
    actions = cursor.fetchall()
    cursor.close()
    print('actions=', actions)
    return actions
#*********************************************************************************************************************************
'''def add_commentaire_opportunite(id_opp,id_user,comment,style,cnx):
    try:
        print('add')
        rv = get_commentaire_prospect(id_opp, id_user, comment, style, cnx)
        print('rv', rv)
        if rv:
            response =rv[0][0]
        else:
            sql ="INSERT INTO commentaire_opportunite set  opp=%s , user=%s ,commentaire=%s, style=%s "
            cur = cnx.cursor()
            cur.execute(sql, (id_opp, id_user, comment, style,))
            rv = get_commentaire_prospect(id_opp, id_user, comment, style, cnx)
            print('rv',rv)
            cnx.commit()
            cur.close()
            if rv:
                response = rv[0][0]
            else:
                response = ''
        return response
    except:
        print('except')'''
#*********************************************************************************************************************************
def get_commentaire_opportunite(id_opp, id_user, comm, style,cnx):
    try:
        cursor = cnx.cursor()
        rowcount = ('select * from commentaire_opportunite where opp= %s and user= %s and commentaire= %s and style= %s')
        cursor.execute(rowcount, (id_opp, id_user, comm, style,))
        actions = cursor.fetchall()
        cursor.close()
        print('actions=', actions)
        if actions:
            return actions[0][0]
        else:
            return ''
    except:
        print('except')
#********************************************************************************************************************************
def get_idpros_md5(id,cnx):
    print('get_idpros')
    cursor = cnx.cursor()
    rowcount = ('select * from prospects where md5(id)= %s')
    cursor.execute(rowcount, (id,))
    actions = cursor.fetchall()
    cursor.close()
    print('actions=',actions)
    return actions
#*********************************************************************************************************************************
def Addaction(result, user_id, etat_rdv_id, id_pros, commentaire_action, comm_opp,cnx):
    print(result, user_id, etat_rdv_id, id_pros, commentaire_action, comm_opp)
    try:
        cursor = cnx.cursor()
        query_opp = "SELECT opportunite.type_opp, opportunite.start FROM opportunite WHERE id =%s"

        cursor.execute(query_opp, (result,))
        actions = cursor.fetchall()
        #cursur=bind_result(type,start)
        cursor.close()
        type_opp=actions[0][0]
        print(type_opp)
        start=actions[0][1]
        print(start)
        print('actions=', actions)
        if (type_opp != 4 and start != None and start != "null" and start != "0000-00-00 00:00:00") :
            cursor = cnx.cursor()
            print('true')
            query = 'INSERT INTO `interface`.`actions`(`action`, `opp`, `pros`, `user`, `commentaire`, `comm_opp`,`date_objectif`) VALUES (%s,%s,%s,%s,%s,%s,%s)'
            print('tr')
            print(query)
            print(etat_rdv_id, result, id_pros, user_id, commentaire_action, comm_opp, start)
            cursor.execute(query, (etat_rdv_id, result, id_pros, user_id, commentaire_action, comm_opp, start,))
            #cursor.execute(query, ('0', '160337', '445808', '578', 'Modifications fiche sans changement de statut', 'test commentaire opportunité', '2017-06-06 14:00:43'))
            print('done')
            cursor.close()

        else :
            print('false')
            query = 'INSERT INTO `interface`.`actions` (`action`, `opp`, `pros`, `user`, `commentaire`, `comm_opp`) VALUES (%s, %s,%s, %s,%s, %s)'
            cursor.execute(query, (etat_rdv_id, result, id_pros, user_id, commentaire_action, comm_opp,))


        cursor.close()
        return True
    except:
        return False
#*********************************************************************************************************************************
def list_document(id,cnx):
    #try:
    print('list_document_contrat')
    cur = cnx.cursor()
    rowcountall = cur.callproc('list_document_contrat', (id,))
    list_aff = []
    print('debfor')
    for result in cur.stored_results():
        global results1
        results1 = result.fetchall()
        for j in results1:
            list_aff.append(j)
    cur.close()
    print(list_aff)
    return list_aff

    #except:
    #    print('except')
    #   cnx = mariadb.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019', database='interface',port=1433)
#*********************************************************************************************************************************
def get_id_contrat_md5(id,cnx):
    print('get_id_contrat')
    cursor = cnx.cursor()
    rowcount = ('SELECT id from contrat where md5(id) = %s')
    cursor.execute(rowcount, (id,))
    actions = cursor.fetchall()
    cursor.close()
    print('actions=',actions)
    return actions
#*********************************************************************************************************************************
def get_id_affaire_md5(id,cnx):
    print('get_id_affaire')
    cursor = cnx.cursor()
    rowcount = ('SELECT id from affaire where md5(id) =  %s')
    cursor.execute(rowcount, (id,))
    actions = cursor.fetchall()
    cursor.close()
    print('actions=', actions)
    return actions


def get_id_document_md5(id,cnx):
    cursor = cnx.cursor()
    print('get_id_doc')
    rowcount = ('SELECT id from type_document where md5(id) = %s')
    cursor.execute(rowcount, (id,))
    actions = cursor.fetchall()
    cursor.close()
    print('actions=', actions)
    return actions
#*********************************************************************************************************************************

#*********************************************************************************************************************************
def get_file_action(type,id,cnx):
    try:
        cursor = cnx.cursor()
        rowcount = ('SELECT * FROM fichier_action where %s = %s')
        cursor.execute(rowcount, (type, id,))
        actions = cursor.fetchall()
        cursor.close()
        print('actions=', actions)
        return actions
    except:
        print('except')
#*********************************************************************************************************************************
def list_category_user(id_user,cnx):
    cursor = cnx.cursor()
    rowcount = ('SELECT categorie_libelle_color FROM roles_cat_statut WHERE md5(users_id)= %s')
    cursor.execute(rowcount, (id_user,))
    actions = cursor.fetchall()
    cursor.close()
    print('actions=',actions)
    return actions

def getallopportunite_event_negoci(collaborateur, start, end, id_cat,cnx):
    cursor = cnx.cursor()
    print('deb_f')
    rowcount = ('SELECT opportunite_type.libelle as type_opp_lib,(select group_concat(tags.libelle SEPARATOR "|") from tags where FIND_IN_SET(tags.id,opportunite.tags)>0) as TAGS_opp,etat_opp.couleur_police,campagnes.icon as campicon,opportunite.*,etat_opp.color,etat_opp.etat,etat_opp.classe,prospects.name,prospects.surname,prospects.tel,prospects.mobile,adresses.CP,villes.nom_comm,campagnes.libelle,complement_adr,streetNumber,streetName,dossier.mca,cmp.denomination,prospects.DN,opportunite.date_depot FROM opportunite LEFT JOIN dossier on opportunite.id = dossier.id_opp and dossier.id_contrat is null LEFT JOIN cmp on dossier.cmp =cmp.siren left join opportunite_type on opportunite.type_opp = opportunite_type.id,etat_opp,prospects,adresses,villes,campagnes WHERE etat_opp.id in(2,4,6,55,81,28,33,532,201,202,530,251,252,253,265,266,32,213,204,103,104,418,77,78,430,431,432,254,255,529) and  opportunite.etat_rdv_id=etat_opp.id AND opportunite.prospects_id=prospects.id AND adresses.id=prospects.loaction AND villes.id=adresses.ville AND campagnes.id=opportunite.campagne_id AND ((md5(commerciaux_id)= %s AND start BETWEEN %s AND %s AND ( etat_opp.id in (select id_statut from structure_statuts_opp_subquery where id_service = %s))))')
    print('f2')
    cursor.execute(rowcount, (collaborateur, start, end, id_cat,))
    print(cursor.fetchall())
    print('f3')
    actions = cursor.fetchall()
    print('actions',actions)
    print('f4')
    cursor.close()
    return actions


def  getall_event(collaborateur, start, end,cnx):
    try:
        cursor = cnx.cursor()
        rowcount = ('SELECT *, DATE_FORMAT(date_debut, "%W") AS Madate FROM event_user WHERE(md5(id_user) =%s AND (((date_debut  BETWEEN %s AND %s)OR(date_fin BETWEEN %s AND %s))OR((%s  BETWEEN date_debut AND date_fin)OR(%s BETWEEN date_debut AND date_fin))))')
        cursor.execute(rowcount, (collaborateur, start, end, start, end, start, end,))
        actions = cursor.fetchall()
        cursor.close()
        print(actions)
        return actions
    except:
        print('except')



def  getall_not(collaborateur, start, end,cnx):
    while True:
        try:
            cursor = cnx.cursor()
            rowcount = ('SELECT * from notifications where (md5(user) = %s AND date_notification BETWEEN %s AND %s and status = 1)')
            cursor.execute(rowcount, (collaborateur, start, end,))
            actions = cursor.fetchall()
            cursor.close()
            return actions
            break
        except:
            return actions
            cnx = mariadb.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)



def autorization(api_key=None, mail=None, id=None):
    while True:
        try:
            cursor = cnx.cursor()
            rowcount = ('SELECT id from users WHERE (api_key = %s and mail =%s) or id_session = %s')
            cursor.execute(rowcount, (api_key, mail, id,))
            actions = cursor.fetchall()
            cursor.close()
            if actions:
                return True
            else:
                return False
            break
        except:
            cnx = mariadb.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)

def get_all_user_id(idd=None, id_session=None):
    while True:
        try:
            cursor = cnx.cursor()
            query = ("SELECT id ,role from users where  MD5(id)= %s or  id_session= %s")
            cursor.execute(query, (idd, id_session,))
            pw = cursor.fetchall()
            cursor.close()
            iduser = 0
            idrole = 0
            for i in pw:
                iduser = i[0]
                idrole = i[1]
            return iduser, idrole
            break
        except:
            cnx =mariadb.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)


def get_visivilite_affaire(categorie, idrole):
    while True:
        try:
            cursor = cnx.cursor()
            query = ("SELECT visibilite FROM roles_categoryStatus_Doss where role = %s AND category = %s")
            cursor.execute(query, (idrole, categorie,))
            actions = cursor.fetchall()
            cursor.close()
            visibilite = -1
            for i in actions:
                visibilite = i[0]
            return visibilite
            break
        except:
            cnx = mariadb.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',
                                  database='interface', port=1433)


def get_date_action_doss(id):
    while True:
        try:
            cursor = cnx.cursor()
            rowcount = ("select CAST(date AS DATE) as date from actions_dossier WHERE actions_dossier.dossier = %s and action is not NULL ORDER BY date desc LIMIT 1")
            cursor.execute(rowcount, (str(id),))
            actions = cursor.fetchall()
            cursor.close()
            date = ""
            for i in actions:
                date = i[0]
            return date
            break
        except:
            mariadb.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)


def mres(value):
    search = ["\\", "\x00", "\n", "\r", "'", '"', "\x1a"]
    replace = ["\\\\", "\\0", "\\n", "\\r", "''", '\"', "\\Z"]
    for i, j in zip(search, replace):
        value = value.replace(i, j)
    return value


def execute_req(req):
    while True:
        try:
            cursor = cnx.cursor()
            cursor.execute(req)
            pw = cursor.fetchall()
            cursor.close()
            return pw
            break
        except:
            mariadb.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)


def replace_true_rows_names(chaine):
    names = ["opportunite_id", "dataform_prod", "opportunite_etat", "opportunite_users_id",
             "opportunite_commerciaux_id", "opportunite_start", "opportunite_end", "opportunite_description",
             "opportunite_enregistrement", "opportunite_prospects_id", "opportunite_date_depot", "opportunite_reported",
             "opportunite_log", "opportunite_etat_rdv_id", "opportunite_last_update", "users_mail", "organismes_nom",
             "organismes_id_type", "type_entreprise_libelle", "commerciaux_nom", "commerciaux_prenom",
             "commerciaux_mail", "commerciaux_code", "prospects_surname", "prospects_name", "prospects_tel",
             "prospects_description", "prospects_adresse_mail", "prospects_mobile", "prospects_tel2",
             "prospects_first_campagne", "prospects_last_campagne", "prospects_loaction", "adresses_adresse",
             "adresses_complement_adr", "adresses_latitude", "adresses_streetName", "adresses_streetNumber",
             "adresses_longitude", "adresses_ville", "villes_postal_code", "villes_nom_dept", "villes_nom_region",
             "villes_id", "etat", "adresses_CP", "campagnes_libelle", "users_nom", "users_prenom", "first_campagne",
             "last_campagne", "streetNumber", "streetName", "commercial_zone", "groupe_collab_id", "groupe_collab_nom",
             "groupe_collab_description", "manager_id", "commerciaux_zone", "ville.geo_shape_json", "villes_nom_comm",
             "opportunite_type", "opportunite_type_libelle", "campagnes_couleur", "campagne_id", "etat_opp_id",
             "users_manager", "users_role", "categorie_id", "prospects_id", "dossier_type", "dossier_mca",
             "dossier_mcm", "dossier_ech_res", "dossier_cmp", "dossier_nom_p", "dossier_reference", "dossier_nb_adh",
             "dossier_frac_p", "dossier_num_contrat", "dossier_garanti", "dossier_note", "dossier_budget",
             "dossier_assure", "dossier_date_creation", "dossier_id_opp", "dossier_id_contrat", "cmp_denomination",
             "campagnes_specifique", "rappel_marque", "version", "energie", "pa", "type_mines", "cnit", "alimentation",
             "nombre_places", "bv_type", "opportunite_version_vehicule", "vehicule", "prospects_fiche_dec",
             "prospects_civ", "prospects_dn", "opportunite_form", "opportunite_object",
             "opportunite_users_enteprise_id", "campagnes_date_demarage", "campagnes_date_arret", "campagnes_script",
             "campagnes_tags", "tags_opp", "users_enterprise_id", "cycle_vie_cmp", "visa_etat_opp", "organismes_type",
             "etat_opp_classe", "prospects_situation", "prospects_nb_enfant", "etat_rdv_color", "cycle_vie",
             "id_doublon", "class_etats_libele", "catergorieStatusOpp_libele", "user_id_suivi_opp",
             "id_produit_campagne", "id_produit_campagne_md5", "campagnes_rdv_multiple", "samedi_off", "heure_fin",
             "form_camp"]
    true_names = ["opportunite.id", "opportunite.data_form_prod", "opportunite.etat", "opportunite.users_id",
                  "opportunite.commerciaux_id", "opportunite.start", "opportunite.end", "opportunite.description",
                  "opportunite.enregistrement", "opportunite.prospects_id", "opportunite.date_depot",
                  "opportunite.reported", "opportunite.log", "opportunite.etat_rdv_id", "opportunite.last_update",
                  "users.mail", "organismes.nom", "organismes.id_type", "type_organisme.libelle", "users1.nom",
                  "users1.prenom", "users1.mail", "users1.code", "prospects.surname", "prospects.name", "prospects.tel",
                  "prospects.description", "prospects.adresse_mail", "prospects.mobile", "prospects.tel2",
                  "prospects.first_campagne", "prospects.last_campagne", "prospects.loaction", "adresses.adresse",
                  "adresses.complement_adr", "adresses.latitude", "adresses.streetName", "adresses.streetNumber",
                  "adresses.longitude", "adresses.ville", "villes.postal_code", "villes.nom_dept", "villes.nom_region",
                  "villes.id", "etat_opp.etat", "adresses.CP", "campagnes.libelle", "users.nom", "users.prenom",
                  "prospects.first_campagne", "prospects.last_campagne", "adresses.streetNumber", "adresses.streetName",
                  "zones.nom", "groupe_collab.id", "groupe_collab.nom", "groupe_collab.description",
                  "groupe_collab.manager", "users.zone", "villes.geo_shape_json", "villes.nom_comm",
                  "opportunite.type_opp", "opportunite_type.libelle", "campagnes.couleur", "opportunite.campagne_id",
                  "etat_opp.id", "user_manager.id_manager", "users.role", "etat_opp.categorie", "prospects.id",
                  "contrat.type", "dossier.mca", "dossier.mcm", "dossier.echeance_resiliation", "dossier.cmp",
                  "dossier.nom_p", "dossier.reference", "dossier.nb_adh", "dossier.Fractionnement_prime",
                  "dossier.num_contrat", "dossier.gar_demande", "dossier.note", "dossier.budget", "dossier.assure",
                  "dossier.date_creation", "dossier.id", "dossier.id_contrat", "cmp.denomination",
                  "campagnes.specifique", "auto_versions.rappel_marque", "auto_versions.version",
                  "auto_versions.energie", "auto_versions.pa", "auto_versions.type_mines", "auto_versions.cnit",
                  "auto_versions.alimentation", "auto_versions.nombre_places", "auto_versions.bv_type",
                  "opportunite.version_vehicule", "campagnes.vehicule", "prospects.fiche_dec", "prospects.civilite",
                  "prospects.DN", "opportunite.form", "opportunite.object", "opportunite.users_entreprise_id",
                  "campagnes.date_demarage", "campagnes.date_arret", "campagnes.script", "campagnes.tags",
                  "opportunite.tags", "users.entreprise_id", "campagnes.cycle_vie", "etat_opp.visa", "organismes.id",
                  "etat_opp.classe", "prospects.situation", "prospects.nb_enfants", "class_etats.color",
                  "etat_opp.cycle_vie", "opportunite.id_doublon", "class_etats.libele", "catergorieStatusOpp.libele",
                  "suivi_opp.id_user", "campagnes.id_produit", "md5(campagnes.id_produit)", "campagnes.rdv_multiple",
                  "users1.samedi_off", "users1.heure_fin", "form_campagne.form"]
    if chaine != None:
        chaine.strip('"\ \t"')
        for i, j in zip(names, true_names):
            chaine = chaine.replace(i, j)
    return chaine


def replace_true_rows_names_aff(chaine):
    names = ["organismes_nom", "affaire_compteur", "game_produit", "contrat_id", "affaire_qualite_1",
             "affaire_comm_qualite_1", "affaire_qualite_2", "affaire_comm_qualite_2", "affaire_qualite_3",
             "affaire_comm_qualite_3", "affaire_qualite_4", "affaire_comm_qualite_4", "affaire_produit_contrat_id",
             "affaire_produit_contrat_id_md", "affaire_produit_contrat", "affaire_produit_code_bareme", "users_id_user",
             "etat", "etat_dossier_id_parent", "etat_dossier_categorie", "etat_dossier_level", "etat_dossier_visa",
             "etat_dossier_dependance", "etat_dossier_sup", "contrat_type", "catergorieStatusDoss_libelle",
             "prospects_name", "prospects_surname", "prospects_tel", "prospects_tel2", "prospects_mobile",
             "prospects_adresse_mail", "prospects_description", "prospects_first_camp", "prospects_last_camp",
             "prospects_location", "prospects_last_update", "adresses_cp", "adresses_id", "adresses_adresse",
             "adresses_complement_adr", "adresses_streetNumber", "adresses_streetName", "adresses_type_adr",
             "adresses_risque", "adresses_id_parent", "ville", "villes_postal_code", "villes_id", "villes_nom_comm",
             "users_nom", "villes_nom_dept", "villes_nom_region", "villes_geo_shape_json", "villes_geo_shape",
             "prospects_id", "adresses_latitude", "adresses_longitude", "cmp_siren", "cmp_denomination", "campagne_id",
             "commercieux_id", "contrat_form", "affaire_id", "affaire_id_contrat", "affaire_id_prospect", " id_user ",
             "affaire_status", "favori_affaire", "opportunite_id", "affaire_mca", "affaire_mcm", "affaire_date_deff",
             "affaire_cmp", "affaire_nom_p", "affaire_reference", "affaire_purc_derg", "affaire_derogation",
             "affaire_nb_adh", "affaire_frac_prime", "affaire_num_contrat", "affaire_occ_res", "affaire_date_rappelle",
             "affaire_note", "affaire_date_creation", "affaire_last_update", "affaire_souscription", "affaire_form",
             "affaire_assure", "affaire_id_dossier", "prospects_fiche_dec", "dossier_an_mca", "dossier_an_mcm",
             "dossier_an_cmp", "dossier_budget", "dossier_garanti_demande", "cmp1_denomination", "prospects_civ",
             "prospects_dn", "dossier_num_contrat", "dossier_echeance_resiliation", "dossier_clt_sodedif",
             "prospects_situation", "prospects_nb_enfant", "etat_dossier_classe", "etat_dossier_color",
             "dossier_nom_produit", "user_id_suivi_affaire", "affaire_mode_paiement", "id_produit_campagne",
             "id_produit_campagne_md5", "form_campagne_opp", "opportunite_prospects_id", "affaire_campagne_libelle",
             "campagnes_couleur", "class_etats_libele", "affaire_parent", "produit_sante_option",
             "produit_sante_renfort", "produit_frais_cie", "produit_frais_sodeif", "opportunite_object",
             "object_affaire", "affaire_data_form_prod", "commerciaux_nom", "commerciaux_prenom", "game_nom",
             "id_affaire", "entreprise_id"]
    true_names = [" `organismes`.`nom` ", " `affaire`.`compteur` ", " `produit_sante`.`game` ",
                  " `affaire`.`id_contrat` ", " `affaire`.`qualite_1` ", " `affaire`.`comment_q1` ",
                  " `affaire`.`qualite_2` ", " `affaire`.`comment_q2` ", " `affaire`.`qualite_3` ",
                  " `affaire`.`comment_q3` ", " `affaire`.`qualite_4` ", " `affaire`.`comment_q4` ",
                  " `produit_sante`.`id` ", " md5(`produit_sante`.`id`) ", " `produit_sante`.`nom_produit` ",
                  " `produit_sante`.`code_bareme` ", " `users`.`id` ", " `etat_dossier`.`etat` ",
                  " `etat_dossier`.`id_p` ", " `etat_dossier`.`categorie` ", " `etat_dossier`.`level` ",
                  " `etat_dossier`.`visa` ", " `etat_dossier`.`dependance` ", " `etat_dossier`.`sup` ",
                  " `contrat`.`type` ", " `catergorieStatusDoss`.`libele` ", " `prospects`.`name` ",
                  " `prospects`.`surname` ", " `prospects`.`tel` ", " `prospects`.`tel2` ", " `prospects`.`mobile` ",
                  " `prospects`.`adresse_mail` ", " `prospects`.`description` ", " `prospects`.`first_campagne` ",
                  " `prospects`.`last_campagne` ", " `prospects`.`loaction` ", " `prospects`.`last_update` ",
                  " `adresses`.`CP` ", " `adresses`.`id` ", " `adresses`.`adresse` ", " `adresses`.`complement_adr` ",
                  " `adresses`.`streetNumber` ", " `adresses`.`streetName` ", " `adresses`.`type_adr` ",
                  " `adresses`.`risque` ", " `adresses`.`id_parent` ", " `adresses`.`ville` ",
                  " `villes`.`postal_code` ", " `villes`.`id` ", " `villes`.`nom_comm` ", " `villes`.`nom_dept` ",
                  " `villes`.`nom_region` ", " `villes`.`geo_shape_json` ", " `villes`.`geo_shape` ",
                  " `prospects`.`id` ", " `adresses`.`latitude` ", " `adresses`.`longitude` ", " `cmp`.`siren` ",
                  " `cmp`.`denomination` ", " `cmp`.`denomination` ", " `affaire`.`id_camp` ",
                  " `opportunite`.`commerciaux_id` ", " `contrat`.`form` ", " `affaire`.`id` ",
                  " `affaire`.`id_contrat` ", " `affaire`.`id_prospect` ", " `affaire`.`id_user` ",
                  " `affaire`.`status` ", " `affaire`.`favori` ", " `affaire`.`id_opp` ", " `affaire`.`mca` ",
                  " `affaire`.`mcm` ", " `affaire`.`date_deff` ", " `affaire`.`cmp` ", " `affaire`.`nom_p` ",
                  " `affaire`.`reference` ", " `affaire`.`pourc_derg` ", " `affaire`.`derogation` ",
                  " `affaire`.`nb_adh` ", " `affaire`.`Fractionnement_prime` ", " `affaire`.`num_contrat` ",
                  " `affaire`.`occ_resiliation` ", " `affaire`.`date_rapelle` ", " `affaire`.`note` ",
                  " `affaire`.`date_creation` ", " `affaire`.`last_update` ", " `affaire`.`souscription` ",
                  " `affaire`.`form` ", " `affaire`.`assure` ", " `affaire`.`id_dossier` ", " `prospects`.`fiche_dec` ",
                  " `dossier`.`mca` ", " `dossier`.`mcm` ", " `dossier`.`cmp` ", " `dossier`.`budget` ",
                  " `dossier`.`gar_demande` ", " `cmp1`.`denomination` ", " `prospects`.`civilite` ",
                  " `prospects`.`DN` ", " `dossier`.`num_contrat` ", " `dossier`.`echeance_resiliation` ",
                  " `dossier`.`clt_sodedif` ", " `prospects`.`situation` ", " `prospects`.`nb_enfants` ",
                  " `etat_dossier`.`classe` ", " `class_etats`.`color` ", " `dossier`.`nom_produit` ",
                  " `suivi_affaire`.`id_user` ", " `affaire`.`mode_paiement` ", " `campagnes`.`id_produit`",
                  " md5(`campagnes`.`id_produit`) ", " `campagnes`.`form` ", " `affaire`.`id_prospect` ",
                  " `campagnes`.`libelle` ", " `campagnes`.`couleur` ", " `class_etats`.`libele` ",
                  " `affaire`.`affaire_parent` ", " `produit_sante`.`option` ", " `produit_sante`.`renfort` ",
                  " `produit_sante`.`frais_cie` ", " `produit_sante`.`frais_sodedif` ", " `opportunite`.`object` ",
                  " `affaire`.`object_affaire` ", " `opportunite`.`data_form_prod` ", " `users1`.`nom` ",
                  " `users1`.`prenom` ", " `game_prod`.`nom` ", " `affaire`.`id` ",
                  " `opportunite`.`users_entreprise_id` "]
    if chaine != None:
        chaine.strip('"\ \t"')
        for i, j in zip(names, true_names):
            chaine = chaine.replace(i, j)
    return chaine


def get_tags_opp():
    while True:
        try:
            cursor = cnx.cursor()
            rowcount = cursor.execute("SELECT * FROM tags")
            pw = cursor.fetchall()
            cursor.close()
            return pw
            break
        except:
            cnx = mariadb.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)


def callaffaires(args):
    while True:
        try:
            cur = cnx.cursor()
            rowcountall = cur.callproc('ListingAffPerUser_dev', args)
            list_aff = []
            for result in cur.stored_results():
                global results1
                results1 = result.fetchall()
                for j in results1:
                    list_aff.append(j)
            cur.close()
            return list_aff
            break
        except:
            cnx = mariadb.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019', database='interface', port=1433)


def callcommuniques(args):
    while True:
        try:
            cur = cnx.cursor()
            rowcountall = cur.callproc('list_communiques', args)
            print(rowcountall)
            list_aff = []
            for result in cur.stored_results():
                global results1
                results1 = result.fetchall()
                for j in results1:
                    list_aff.append(j)
            cur.close()
            return list_aff
            break
        except:
            cnx =mariadb.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)


def call(args):
    while True:
        try:
            cur = cnx.cursor()
            rowcountall = cur.callproc('lisntingOppPerUser_list_test', args)
            list_opp = []
            for result in cur.stored_results():
                global results1
                results1 = result.fetchall()
                for j in results1:
                    list_opp.append(j)
            cur.close()
            return list_opp
            break
        except:
            cnx = mariadb.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)


def test_access(id_user, etat_opp_id, affichage, cycle, phase):
    respense = []
    # test=[]
    cat = list_category_user(id_user)
    testdisabled = 0
    for i, n in enumerate(cat):
        categorie = cat[i]
        id_cat = categorie[0]
        sup_cat = categorie[-1]
        etat_qyery = list_action_categorie_test(id_cat, cycle)
        for etat in etat_qyery:
            if (etat[3] != None or etat[3] == 0):
                id_etat = etat[3]
                sup_etat = etat[2]
                test = action_super_test(sup_cat, sup_etat)
                if (id_etat != '' and test == True):
                    if (affichage == True and (etat[1] == None or etat[1] == None)):
                        if ((etat[0] != None and etat_opp_id != etat[0]) or (etat[4] != phase) or (
                                etat_opp_id == etat[3])):
                            # respense['test'] = 'true'
                            respense.append("-1")
                        else:
                            testdisabled += 1
                        # respense['test'] = 'true'
                        # respense.append("*")
    return testdisabled


'''def list_category_user(id_user):
    while True:
        try:
            print('deb')
            cursor = cnx.cursor()
            query = ("SELECT categorie_libelle_color FROM roles_cat_statut WHERE users_id= %s")
            cursor.execute(query, (id_user,))
            pw = cursor.fetchall()
            cursor.close()
            print('pw=',pw)
            str1 = ','.join(pw[0])
            print('str1',str1)
            cat = str1.split('|')
            print('cat')
            return cat
            break
        except:
            print('hi')
            cnx = mariadb.connect(host='dbm2.interface-crm.com', user='', password='', database='interface', port=1433)
'''

def list_action_categorie_test(categorie, cycle):
    while True:
        try:
            cursor = cnx.cursor()
            query = (
                "SELECT dependance as dependance ,id_p as id_p,etat_opp.sup as sup,etat_opp.id as etat_opp_id, etat_opp.categorie as cat FROM etat_opp LEFT JOIN class_etats on etat_opp.classe = class_etats.id  WHERE (categorie=%s and cycle_vie = %s)")
            cursor.execute(query, (categorie, cycle,))
            actions = cursor.fetchall()
            cursor.close()
            return actions
            break
        except:
            cnx =mariadb.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)

def action_super_test(sup_cat, sup_etat):
    if (sup_cat == 0 and sup_etat == 1):
        test = False
    else:
        test = True
    return test


def exist_audio_opp(id):
    while True:
        try:
            cursor = cnx.cursor()
            query = ("SELECT count(*) FROM actions WHERE actions.commentaire LIKE '%%audio%%' and actions.opp = %s")
            cursor.execute(query, (id,))
            actions = cursor.fetchall()
            cursor.close()
            for i in actions:
                count = i[0]
            return count
            break
        except:
            cnx = mariadb.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)


def get_date_action_opp(id):
    while True:
        try:
            cursor = cnx.cursor()
            rowcount = ("select CAST(date AS DATE) as date from actions WHERE actions.opp = %s and action is not NULL ORDER BY date desc LIMIT 1")
            cursor.execute(rowcount, (id,))
            actions = cursor.fetchall()
            cursor.close()
            date = ""
            for i in actions:
                date = i[0]
            return date
            break
        except:
            cnx = mariadb.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)


def get_type_relation(id_opp):
    while True:
        try:
            cursor = cnx.cursor()
            rowcount = (
                "SELECT type_r_opp.icon FROM type_r_opp WHERE type_r_opp.id IN ( SELECT ralation_opp.type_relation FROM ralation_opp WHERE ralation_opp.id_opp1 =%s OR ralation_opp.id_opp2 =%s) LIMIT 1")
            cursor.execute(rowcount, (id_opp, id_opp))
            actions = cursor.fetchall()
            cursor.close()
            icon = ""
            for i in actions:
                icon = i[0]
            return icon
            break
        except:
            cnx =mariadb.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',
                                  database='interface', port=1433)


def get_pros_double(num, type, id_opp):
    while True:
        try:
            cursor = cnx.cursor()
            rowcount = (
                'SELECT IF((%s != "" and %s != "0033000000000" and REPLACE(%s,"_","a") not like "%%a%%"),(select group_concat(DISTINCT prospects.id SEPARATOR "|") from opportunite left join prospects on opportunite.prospects_id = prospects.id where (prospects.mobile = %s OR prospects.tel = %s OR prospects.tel2 = %s) and opportunite.id != %s ),"") as pros_double')
            cursor.execute(rowcount, (str(num), str(num), str(num), str(num), str(num), str(num), id_opp))
            actions = cursor.fetchall()
            cursor.close()
            for i in actions:
                pros_double = i[0]
            return pros_double
            break
        except:
            cnx = mariadb.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019',database='interface', port=1433)


def get_users_opp_suivi(id_opp):
    while True:
        try:
            cursor = cnx.cursor()
            rowcount = ("select suivi_opp.id_user from suivi_opp where id_opp = %s")
            cursor.execute(rowcount, (id_opp,))
            actions = cursor.fetchall()
            iduser = []
            for i in actions:
                iduser.append(i[0])
            cursor.close()
            return iduser
            break
        except:
            cnx = mariadb.connect(host='dbm2.interface-crm.com', user='SOUHA', password='SOUHA@2019', database='interface', port=1433)