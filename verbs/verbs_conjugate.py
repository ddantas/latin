# -*- coding: utf-8 -*-

import re
import yaml
import common as c
import shoebot
import sys
import time


def concat_group(group):
    retval = u""
    for j in range(len(group)):
        if (j == 0):
            retval += group[0]
        else:
            retval += "|"
            retval += group[j]
    return retval
    

def search_group_index(groups, group_name):
    for j in range(len(groups)):
        one_group = groups[j].split(u'|')
        if (one_group[0] == group_name):
            return j
    return -1

def search_mood_index(rules, mood):
    for i in range(len(rules['rules'])):
        if (rules['rules'][i]['mood'] == mood):
            return i
    return -1
    
def strip_spaces(rules):
    for i in range(len(rules['rules'])):
        groups = rules['rules'][i]['groups']
        for j in range(len(groups)):
            rules['rules'][i]['groups'][j] = \
                re.sub('[\s]*\|[\s]*', '|', rules['rules'][i]['groups'][j])
    
def merge_rules(retval, rules):
    retval['label'] = rules['label']
    for i in range(len(rules['rules'])):
        print "====================\n\n"
        mood = rules['rules'][i]['mood']
        groups = rules['rules'][i]['groups']
        i_ret = search_mood_index(retval, mood)
        if (i_ret == -1):
            print "Error: mood {} not found in rule set".format(mood)
            exit(0)
        print "i_ret = {}".format(i_ret)
        print retval['rules'][i_ret]['groups']
        
        for j in range(len(groups)):
            one_group = groups[j].split(u'|')
            print u"{} - {}".format(j, one_group[0])
            j_ret = search_group_index(retval['rules'][i_ret]['groups'], one_group[0])
            if (j_ret == -1):
                print "Error: tense {} not found in rule set".format(one_group[0])
                exit(0)
            print u"j_ret = {}".format(j_ret)
            ret_group = retval['rules'][i_ret]['groups'][j_ret].split(u'|')
            for k in range(len(one_group)):
                print u"<<<{}>>>".format(one_group[k])
                if (one_group[k]):
                    ret_group[k] = one_group[k]
            retval['rules'][i_ret]['groups'][j_ret] = concat_group(ret_group)

def rules_from_paradigm(conjdata, paradigm):
    arr_paradigm = paradigm.split(u'|')
    for k in range(len(arr_paradigm)):
        print arr_paradigm[k]
        if (k == 0):
            retval = conjdata[arr_paradigm[k]]
            strip_spaces(retval)
        else:
            rules = conjdata[arr_paradigm[k]]
            strip_spaces(rules)
            merge_rules(retval, rules)
    return retval
            

    

def split_header(word):
    sign      = re.match(r"\{?(-?).*?\}?.*", word)
    radical   = re.match(r"\{?-?(.*?)\}?\[.*?\]", word)
    desinence = re.match(r"\{?.*?\}?\[(.*?)\]", word)
    print "SIGN"
    txt_sign = ''
    if (type(sign) != type(None)):
        txt_sign = sign.group(1)
    print "DESINENCE"
    txt_desinence = ''
    if (type(desinence) != type(None)):
        txt_desinence = desinence.group(1)
    print "RADICAL"
    txt_radical = ''
    if (type(radical) != type(None)):
        txt_radical = radical.group(1)
    return [txt_sign, txt_radical, txt_desinence]

def color_from_mood(mood):
    if (re.search("Infinitive", mood)):
        return "#42b314"
    if (re.search("Participle", mood)):
        return "#b2640a"
    if (re.search("Gerund", mood)):
        return "#a020cb"
    if (re.search("Imperative", mood)):
        return "#04aba5"
    if (re.search("Subjunctive", mood)):
        return "#2075cb"
    if (re.search("Indicative", mood)):
        return "#cb202c"
    return "#cb202c"

def replace_radical(word, list_rpres, list_rinf, list_rperf, list_rsup):
    word = re.sub(r"RPRES", list_rpres[1], word)
    word = re.sub(r"RINF",  list_rinf[1], word)
    word = re.sub(r"RPERF", list_rperf[1], word)
    word = re.sub(r"RSUP",  list_rsup[1], word)
    return word

def conjugate(rules, list_rpres, list_rinf, list_rperf, list_rsup, label=""):
  #print rules[0]
  txt = u""
  txt += u"name: {}{}\n".format(list_rpres[1], list_rpres[2])

  print u"=========={}".format(txt)
  
  txt += u"label: {}\n".format(label)
  txt += u"updated: {}\n".format(time.strftime("%d %B %Y"))
  txt += u"example_word: \""
  if (list_rpres[2]):
    txt += u"{}{}[{}], ".format(list_rpres[0], list_rpres[1], list_rpres[2])
  else:
    txt += u"{}{}, ".format(list_rpres[0], list_rpres[1])
  if (list_rinf[2]):
    txt += u"{}{}[{}], ".format(list_rinf[0], list_rinf[1], list_rinf[2])
  else:
    txt += u"{}{}, ".format(list_rinf[0], list_rinf[1])
  if (list_rperf[2]):
    txt += u"{}{}[{}], ".format(list_rperf[0], list_rperf[1], list_rperf[2])
  else:
    txt += u"{}{}, ".format(list_rperf[0], list_rperf[1])
  if (list_rsup[2]):  
    txt += u"{}{}[{}]\"\n".format(list_rsup[0], list_rsup[1], list_rsup[2])
  else:
    txt += u"{}{}\"\n".format(list_rsup[0], list_rsup[1])

  #print u"LEN(RULES) = {}".format(len(rules))

  for i in range(len(rules)):
    if (i == 0):
      txt += u"left:\n"
    elif (i == len(rules) / 2):
      txt += u"right:\n"
    
    mood = rules[i]['mood']
    mood.decode('utf-8')
    #print u"Mood = {}".format(mood)
    txt += u"  - title: {}\n".format(mood)
    txt += u"    fill: \"{}\"\n".format(color_from_mood(mood))
    txt += u"    groups:\n"
    groups = rules[i]['groups']
    #print u"Groups = {}".format(len(groups))
    
    for j in range(len(groups)):
      one_group = groups[j].split(u'|')
      txt += u"      - \""
      for k in range(len(one_group)):
        if (k != 0):
          txt += " | "

        word = replace_radical(one_group[k], list_rpres, list_rinf, list_rperf, list_rsup)
        #print u"* {}".format(word)
        txt += word
      txt += u"\"\n"

  return txt


infinitive = sys.argv[1] 
outputfile = sys.argv[2]
listfile = "verbs_data/latin_verbs_list.yaml"
conjfile = "verbs_data/latin_verbs_conj.yaml"

print "Infinitive = {}".format(infinitive)
print "Output file = {}".format(outputfile)
print "Conjugation data file = {}".format(conjfile)

with open(conjfile, "r") as f:
    conjtxt = unicode(f.read(), 'utf-8', errors='ignore')
    conjdata = yaml.load(conjtxt)
    f.close()

with open(listfile, "r") as f:
    listtxt = unicode(f.read(), 'utf-8', errors='ignore')
    listdata = yaml.load(listtxt)
    f.close()

#print conjtxt #.encode("utf-8")
#print listtxt #.encode("utf-8")

#print listdata

list_header = listdata[infinitive]
print list_header
print list_header['inf']
print list_header['pres']
print list_header['perf']
print list_header['sup']
print list_header['paradigm']

list_rpres = split_header(list_header['pres'])
print u"RPRES = {}{}[{}]".format(list_rpres[0], list_rpres[1], list_rpres[2])
list_rinf = split_header(list_header['inf'])
print u"RINF = {}{}[{}]".format(list_rinf[0], list_rinf[1], list_rinf[2])
list_rperf = split_header(list_header['perf'])
print u"RPERF = {}{}[{}]".format(list_rperf[0], list_rperf[1], list_rperf[2])
list_rsup = split_header(list_header['sup'])
print u"RSUP = {}{}[{}]".format(list_rsup[0], list_rsup[1], list_rsup[2])

paradigm = list_header['paradigm']

#one_conjdata = conjdata[paradigm]
one_conjdata = rules_from_paradigm(conjdata, paradigm)

label = one_conjdata['label']
rules = one_conjdata['rules']
print "LABEL = {}".format(label)
print "RULES = {}".format(rules)

result = conjugate(rules, list_rpres, list_rinf, list_rperf, list_rsup, label)
print result.encode("utf-8")


with open(outputfile, "w") as f:
  f.write(result.encode("utf-8"))
  f.close()





