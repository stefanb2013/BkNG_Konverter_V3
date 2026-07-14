<<<<<<< HEAD
import tkinter as tk
from tkinter import filedialog
import re
import sys


class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)  # automatisch scrollen

    def flush(self):
        pass  # notwendig für sys.stdout


ErwAusgabe = 0

def select_file(entry, var_name):
    filepath = filedialog.askopenfilename()
    if filepath:
        entry.delete(0, tk.END)
        entry.insert(0, filepath)

        global PathDpList, PathGruppen, PathGlobalOld, PathGlobalNew
        if var_name == "dp":
            PathDpList = filepath
        elif var_name == "gruppen":
            PathGruppen = filepath
        elif var_name == "old":
            PathGlobalOld = filepath
        elif var_name == "new":
            PathGlobalNew = filepath

def start_conversion():

    ersterDPgefunden=0
    GruppeFehlt = 0
    ParString = ""
    PabString = ""
    KtxString = ""
    Gruppenzaehler = 0
    DPzaehler = 0
    Varzaehler = 0
    DPzaehlerErstellung = 0
    bBlockGefunden = 0
    PabBlockIndex = 0
    VisBlockIndex = 0
    VarIndex = 0
    dictGruppen = {"Datenpunkt" : "Gruppe"}
    dictVarType = {"Datenpunkt" : "VarType"}
    dictVarComment= {"Datenpunkt" : "Kommentar"}
    dictDPs = {"Datenpunkt" : "Parameter"}
    dictPabBlock = {"Datentyp":"Blockdef"}
    dictVisBlock = {"Datentyp":"Blockdef"}
    VarList = ["Variable"]
    PabBlockList  = ["Variable"]
    VisBlockList  = ["Variable"]


    print("Starte Konvertierung...")
    print("PathDpList:", PathDpList)
    print("PathGruppen:", PathGruppen)
    print("PathGlobalOld:", PathGlobalOld)
    print("PathGlobalNew:", PathGlobalNew)


###########################################################################################################


   
    fDplistIN = open(PathDpList, "r")
    fGruppenIN = open(PathGruppen, "r")
    fVarIN = open(PathGlobalOld, "r")

    fVarOUT = open(PathGlobalNew, "w")

    # Dictionary für Gruppen erstellen

    if (ErwAusgabe == "j"):
      print("Konvertierung gestartet\n")


    if (ErwAusgabe == "j"):
      print("Global.var aus altem Projekt wird durchsucht\n")


    for lineVar in fVarIN:
       
      if "VAR" not in lineVar and "(*" not in lineVar[:3] and ":" in lineVar:
           VarName = lineVar[:lineVar.find(":")]
           VarName = VarName.strip()
           VarType = lineVar[lineVar.find(":"):lineVar.find(";")]
           VarType = VarType.strip(" : ")
           VarType = VarType.strip()
           dictVarComment[VarName] = lineVar[lineVar.find("(*"):lineVar.find("*)")+2]
           
           #print(VarComment)
           if (ErwAusgabe == "j"):
              print("Variable gefunden: ",VarName," : ",VarType)
           VarList.append(VarName)
           dictVarType[VarName] = VarType

           VarIndex +=1
    print("\nEs wurden ",VarIndex," Variablen gefunden")   


    print("\nGruppen.dat aus altem Projekt wird durchsucht")

    for lineGruppen in fGruppenIN:

       if "$" in lineGruppen:                         #Gruppe gefunden
           aktGruppe = lineGruppen
           aktGruppe = aktGruppe.strip(" \"@,$\n")             #entfernt Whitespace, ", , @, ...
           Gruppenzaehler += 1
           if (ErwAusgabe == "j"):
              print("Gruppe gefunden: ", aktGruppe)

       if "@" in lineGruppen:                         #DP gefunden
           lineGruppen = lineGruppen[2:]  #entfernt Kommentare
           match = re.search(r"(\")", lineGruppen)
           if match:
               lineGruppen = lineGruppen[:match.start()]
           lineGruppen = lineGruppen.strip(" \"@,")            #entfernt Whitespace, ", , @, ...
           dictGruppen[lineGruppen] = aktGruppe

    #print("dictGruppen: ",dictGruppen)
       
    #dictGruppen.update({"UST_Status" : "Unterstationsstatus"})

    print ("\nEs wurden ",Gruppenzaehler," Gruppe(n) gefunden")


    print("\ndplist.dat aus altem Projekt wird durchsucht:")



    for lineDplist in fDplistIN:

    ############################################



       if "$" in lineDplist:                                       #Blockdefinition gefunden
           bBlockGefunden = 1
           BlockTyp = lineDplist[lineDplist.find("$")+1:lineDplist.find("\n")]
           BlockTyp = BlockTyp[:BlockTyp.find("\"")]
           BlockTyp = BlockTyp.strip()
           BlockTyp = BlockTyp.upper()
           if (ErwAusgabe == "j"):
              print("gefundene Blockdefinition: ",BlockTyp)
           
           
           
       if "#PAB" in lineDplist and bBlockGefunden and len(lineDplist)>8:            #PAB gefunden
           #print(len(lineDplist))
           if (ErwAusgabe == "j"):
              print(lineDplist)
           dictPabBlock[BlockTyp] = lineDplist[:lineDplist.find("\n")]
           dictPabBlock[BlockTyp] = dictPabBlock[BlockTyp].removeprefix("\"#PAB")
           dictPabBlock[BlockTyp] = dictPabBlock[BlockTyp][:dictPabBlock[BlockTyp].find("\"")]
           dictPabBlock[BlockTyp] = dictPabBlock[BlockTyp].strip()
           dictPabBlock[BlockTyp] = dictPabBlock[BlockTyp].replace(" ",", ")
           #print("dictPabBlock ",dictPabBlock)


       if "#VIS" in lineDplist and bBlockGefunden:               #VIS gefunden
           if (ErwAusgabe == "j"):
              print(lineDplist)
           dictVisBlock[BlockTyp] = lineDplist[:lineDplist.find(";")]
           dictVisBlock[BlockTyp] = re.sub(r"\"#VIS\s*","",dictVisBlock[BlockTyp], 1, re.I)
           dictVisBlock[BlockTyp] = dictVisBlock[BlockTyp][:dictVisBlock[BlockTyp].find("\"")]
           dictVisBlock[BlockTyp] = dictVisBlock[BlockTyp].strip()
           dictVisBlock[BlockTyp] = dictVisBlock[BlockTyp].replace(" ",", ")
           #print("dictVisBlock ",dictVisBlock)

      

    ##############################################  
       
       
       if "@" in lineDplist and not ";" in lineDplist[:1] :        # Bk-Datenpunkt gefunden
           bBlockGefunden = 0

           dpname = lineDplist[0:lineDplist.find(";")]
           dpname = dpname.replace("\",","")
           dpname = dpname.strip(" @;\" ")
           dpname = dpname.strip()
           if (ErwAusgabe == "j"):
              print("DP Name gefunden: ",dpname)
           if "UST_Status" in dpname:
               dictGruppen.update({dpname : "Unterstationsstatus"})
               
           ersterDPgefunden=1
           if dpname in dictGruppen:
               ParString = " = (Gruppe=\'" +dictGruppen[dpname] + "\')"
               if "UST_Status" in dpname:
                  ParString = " "
           else:
              if "UST_Status" not in dpname:
                 print("Fehler: ->",dpname," - nicht in gruppen.dat!")
                 print("Es wird \"Undefinert\" als Gruppenname verwendet\n")
                 ParString = " = (Gruppe=\'Undefiniert\')"
                 GruppeFehlt = 1
           #print(ParString)       
           dictDPs[dpname] = ParString

           AktDatentyp = dictVarType.get(dpname,"")
           if (ErwAusgabe == "j"):
              print("DP-Typ: ",AktDatentyp)
           AktDatentyp = AktDatentyp.removeprefix("Bk")
           AktDatentyp = AktDatentyp.upper()


           if AktDatentyp in dictPabBlock: #Blockdefinitionen hinzufügen, wenn vorhanden
               ParString = ParString.replace("Gruppe=\'",dictPabBlock[AktDatentyp] + " ,Gruppe=\'")
           #print("ParString nach Blockdef ",ParString)

           if AktDatentyp in dictVisBlock: #Blockdefinitionen hinzufügen, wenn vorhanden
               ParString = ParString.replace("Gruppe=\'",dictVisBlock[AktDatentyp] + " ,Gruppe=\'")
               ParString = re.sub(r"\( ,","(",ParString, 1, re.I)
           #print("ParString nach Blockdef ",ParString)    


           DPzaehler += 1

           
           
       if "~" in lineDplist:                                       #Klartext gefunden
           KtxString = "Klartext='"
           KtxString += lineDplist.strip("~\", ")
           KtxString = KtxString.strip()
           KtxString = KtxString.replace("\",","',")
           KtxString = KtxString.replace(",","")
           #print("KtxString: ",KtxString)
           ParString = ParString.replace("Gruppe=\'",KtxString + ", Gruppe=\'")
           
           dictDPs[dpname] = ParString
           #print("ParString",ParString)

      
       if "#PAB" in lineDplist and ersterDPgefunden and not bBlockGefunden:               #PAB gefunden
           PabString = lineDplist[:lineDplist.find(";")]
           PabString = PabString.removeprefix("\"#PAB")
           PabString = PabString.strip()
           PabString = re.sub(r"\".*","",PabString, 1, re.I)

           PabBlockList = PabString.split() #Aufteilen der Elemente in #PAB
           #print(PabBlockList)
           #print("PabString aus #PAB ",PabString)

           PabBlockIndex = 0
           while PabBlockIndex < len(PabBlockList):
               PabAttribut = PabBlockList[PabBlockIndex]
               PabAttribut = PabAttribut[:PabAttribut.find("=")]
               PabWert = PabBlockList[PabBlockIndex]


               if re.search(PabAttribut, ParString, re.I):
                   #print("Attribut ",PabWert)
                   ParString = re.sub(PabAttribut+"=[^\s,]+",PabWert,ParString, 1, re.I)
                   #print("ParString ",ParString)
               else:
                   ParString = ParString.replace("Gruppe=\'",PabWert + ", Gruppe=\'")

               PabBlockIndex += 1
     
           dictDPs[dpname] = ParString
     

       if "#VIS" in lineDplist and ersterDPgefunden and len(lineDplist)>9 and not bBlockGefunden: #VIS gefunden und VIS nicht leer
           VisString = lineDplist[:lineDplist.find(";")]
           VisString = VisString.removeprefix("\"#VIS")
           VisString = VisString.strip()
           VisString = re.sub(r"\".*","",VisString, 1, re.I)

           VisBlockList = VisString.split() #Aufteilen der Elemente in #VIS
           #print(VisBlockList)
           #print("VisString aus #VIS ",VisString)

           VisBlockIndex = 0
           while VisBlockIndex < len(VisBlockList):
               VisAttribut = VisBlockList[VisBlockIndex]
               VisAttribut = VisAttribut[:VisAttribut.find("=")]
               #VisAttribut = VisAttribut.title()
               VisWert = VisBlockList[VisBlockIndex]
               
               #print(VisAttribut)

               if re.search(VisAttribut, ParString, re.I):
                   #print("Attribut ",VisWert)
                   ParString = re.sub(VisAttribut+"=[^\s,]+",VisWert,ParString, 1, re.I)
                   #print("ParString ",ParString)
               else:
                   ParString = ParString.replace("Gruppe=\'",VisWert + ", Gruppe=\'")

               VisBlockIndex += 1
           #print("ParString nach #VIS ",ParString) 

             

           dictDPs[dpname] = ParString

       
               
    #print(dictDPs)
    print ("\nEs wurden ",DPzaehler," Burklimat-Datenpunkte gefunden")    
       


    print("\nneue Global.var wird erzeugt")


    fVarOUT.write("VAR\n")
    fVarOUT.write("\tVisUstStat : ARRAY[0..7] OF BOOL;\n")

    VarIndex = 1



    while VarIndex < len(VarList) :

       # Ersetzungen
       # Vorlage für Ersetzungen: Values = re.sub(r"SUCHEN","ERSETZEN",Values, 1 ,re.I)

       Values = dictDPs.get(VarList[VarIndex],"")
       #print("vor Umformatierung: ",Values)

       Values = Values.replace("=",":=")
       #Values = Values.replace("'","\"")
       
           
       Values = re.sub(r"(Y|y).(EINH|Einh|einh)","UnitY",Values, 1, re.I)
       Values = re.sub(r"\w*.(EINH|Einh|einh)","Unit",Values, 1, re.I)
       
       if "BkRk" in dictVarType[VarList[VarIndex]]:
          Values = re.sub(r"w.kpos","KposXW",Values, 1, re.I)
          Values = re.sub(r"w.kpos","KposXW",Values, 1, re.I)
          Values = re.sub(r"y.kpos","KposY",Values, 1, re.I)
          
       Values = re.sub(r"\w*.kpos","Kpos",Values, 1, re.I)
       Values = re.sub(r"Hand:=A","Hand:=0",Values, 1, re.I)
       Values = re.sub(r"Int:=I","Int:=1",Values, 1, re.I)
       Values = re.sub(r"Int:=E","Int:=0",Values, 1, re.I)
       Values = re.sub(r"W.MAX","Wmax",Values, 1, re.I)
       Values = re.sub(r"W.MIN","Wmin",Values, 1, re.I)
       Values = re.sub(r"SW.MAX","SWmax",Values, 1, re.I)
       Values = re.sub(r"SW.MIN","SWmin",Values, 1, re.I)
       Values = re.sub(r"Yrmin","YrMin",Values, 1, re.I)
       Values = re.sub(r"Yrmax","YrMax",Values, 1, re.I)
       Values = re.sub(r"SMAX","Smax",Values, 1, re.I)
       Values = re.sub(r"Wert.T0","BP0_Name",Values, 1, re.I)
       Values = re.sub(r"Wert.T1","BP1_Name",Values, 1, re.I)
       Values = re.sub(r"XWG","Xwg",Values, 1, re.I)
       Values = re.sub(r"BAMAX","BAmax",Values, 1, re.I)
       Values = re.sub(r"SWAUT","SWaut",Values, 1, re.I)
       Values = re.sub(r"BA.T0","BA0_Name",Values, 1, re.I)
       Values = re.sub(r"BA.T1","BA1_Name",Values, 1, re.I)
       Values = re.sub(r"BA.T2","BA2_Name",Values, 1, re.I)
       Values = re.sub(r"BA.T3","BA3_Name",Values, 1, re.I)
       Values = re.sub(r"BA.T4","BA4_Name",Values, 1, re.I)
       Values = re.sub(r"Saus.T0","SB0_Name",Values, 1, re.I)
       Values = re.sub(r"Saus.T1","SB1_Name",Values, 1, re.I)
       Values = re.sub(r"Saus.T2","SB2_Name",Values, 1, re.I)
       Values = re.sub(r"Saus.T3","SB3_Name",Values, 1, re.I)
       Values = re.sub(r"Saus.T4","SB4_Name",Values, 1, re.I)
       Values = re.sub(r"RmgSb.T0","SB0_RmName",Values, 1, re.I)
       Values = re.sub(r"RmgSb.T1","SB1_RmName",Values, 1, re.I)
       Values = re.sub(r"RmgSb.T2","SB2_RmName",Values, 1, re.I)
       Values = re.sub(r"RmgSb.T3","SB3_RmName",Values, 1, re.I)
       
       Values = re.sub(r"Rmg.T0","SBX_RmName",Values, 1, re.I)
       Values = re.sub(r"Rmg.T1","SB0_RmName",Values, 1, re.I)
       Values = re.sub(r"Rmg.T2","SB1_RmName",Values, 1, re.I)
       Values = re.sub(r"Rmg.T3","SBY_RmName",Values, 1, re.I)

       Values = re.sub(r"\"","'",Values, 1, re.I)

       
       if "Unit" in Values: # Die Einheit wird extrahiert und in "..." gesetzt
           Einheit = re.sub(r".*Unit:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", Einheit)
           if match:
               Einheit = Einheit[:match.start()]
           Values = re.sub("Unit:=(\s*)(.+?)(,)","Unit:='" + Einheit + "', ",Values,1, re.I)

       if "UnitY" in Values: # Ersetzung für neues Burklimat
           EinheitY = re.sub(r".*UnitY:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", EinheitY)
           if match:
               EinheitY = EinheitY[:match.start()]
           Values = re.sub("UnitY:=(\s*)(.+?)(,)","UnitY:='" + EinheitY + "', ",Values,1, re.I)


       if "SB0_RmName" in Values: # Ersetzung für neues Burklimat
           SB0_RmName = re.sub(r".*SB0_RmName:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", SB0_RmName)
           if match:
               SB0_RmName = SB0_RmName[:match.start()]
           Values = re.sub("SB0_RmName:=(\s*)(.+?)(,)","SB0_RmName:='" + SB0_RmName + "', ",Values,1, re.I)

       if "SB1_RmName" in Values: # Ersetzung für neues Burklimat
           SB1_RmName = re.sub(r".*SB1_RmName:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", SB1_RmName)
           if match:
               SB1_RmName = SB1_RmName[:match.start()]
           Values = re.sub("SB1_RmName:=(\s*)(.+?)(,)","SB1_RmName:='" + SB1_RmName + "', ",Values,1, re.I)

       if "SB2_RmName" in Values: # Ersetzung für neues Burklimat
           SB2_RmName = re.sub(r".*SB2_RmName:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", SB2_RmName)
           if match:
               SB2_RmName = SB2_RmName[:match.start()]
           Values = re.sub("SB2_RmName:=(\s*)(.+?)(,)","SB2_RmName:='" + SB2_RmName + "', ",Values,1, re.I)

       if "SB3_RmName" in Values: # Ersetzung für neues Burklimat
           SB3_RmName = re.sub(r".*SB3_RmName:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", SB3_RmName)
           if match:
               SB3_RmName = SB3_RmName[:match.start()]
           Values = re.sub("SB3_RmName:=(\s*)(.+?)(,)","SB3_RmName:='" + SB3_RmName + "', ",Values,1, re.I)

       if "SB4_RmName" in Values: # Ersetzung für neues Burklimat
           SB4_RmName = re.sub(r".*SB4_RmName:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", SB4_RmName)
           if match:
               SB4_RmName = SB4_RmName[:match.start()]
           Values = r("SB4_RmName:=(\s*)(.+?)(,)","SB4_RmName:='" + SB4_RmName + "', ",Values,1, re.I)

       if "SBX_RmName" in Values: # Ersetzung für neues Burklimat
           SBX_RmName = re.sub(r".*SBX_RmName:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", SBX_RmName)
           if match:
               SBX_RmName = SBX_RmName[:match.start()]
           Values = re.sub("SBX_RmName:=(\s*)(.+?)(,)","SBX_RmName:='" + SBX_RmName + "', ",Values,1, re.I)

       if "SBY_RmName" in Values: # Ersetzung für neues Burklimat
           SBY_RmName = re.sub(r".*SBY_RmName:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", SBY_RmName)
           if match:
               SBY_RmName = SBY_RmName[:match.start()]
           Values = re.sub("SBY_RmName:=(\s*)(.+?)(,)","SBY_RmName:='" + SBY_RmName + "', ",Values,1, re.I)

           

       if "SB0_Name" in Values: # Ersetzung für neues Burklimat
           SB0_Name = re.sub(r".*SB0_Name:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", SB0_Name)
           if match:
               SB0_Name = SB0_Name[:match.start()]
           Values = re.sub("SB0_Name:=(\s*)(.+?)(,)","SB0_Name:='" + SB0_Name + "', ",Values,1, re.I)

       if "SB1_Name" in Values: # Ersetzung für neues Burklimat
           SB1_Name = re.sub(r".*SB1_Name:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", SB1_Name)
           if match:
               SB1_Name = SB1_Name[:match.start()]
           Values = re.sub("SB1_Name:=(\s*)(.+?)(,)","SB1_Name:='" + SB1_Name + "', ",Values,1, re.I)

       if "SB2_Name" in Values: # Ersetzung für neues Burklimat
           SB2_Name = re.sub(r".*SB2_Name:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", SB2_Name)
           if match:
               SB2_Name = SB2_Name[:match.start()]
           Values = re.sub("SB2_Name:=(\s*)(.+?)(,)","SB2_Name:='" + SB2_Name + "', ",Values,1, re.I)
           
       if "SB3_Name" in Values: # Ersetzung für neues Burklimat
           SB3_Name = re.sub(r".*SB3_Name:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", SB3_Name)
           if match:
               SB3_Name = SB3_Name[:match.start()]
           Values = re.sub("SB3_Name:=(\s*)(.+?)(,)","SB3_Name:='" + SB3_Name + "', ",Values,1, re.I)
           
       if "SB4_Name" in Values: # Ersetzung für neues Burklimat
           SB4_Name = re.sub(r".*SB4_Name:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", SB4_Name)
           if match:
               SB4_Name = SB4_Name[:match.start()]
           Values = re.sub("SB4_Name:=(\s*)(.+?)(,)","SB4_Name:='" + SB4_Name + "', ",Values,1, re.I)

       if "BP0_Name" in Values: # Ersetzung für neues Burklimat
           BP0_Name = re.sub(r".*BP0_Name:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", BP0_Name)
           if match:
               BP0_Name = BP0_Name[:match.start()]
           Values = re.sub("BP0_Name:=(\s*)(.+?)(,)","BP0_Name:='" + BP0_Name + "', ",Values,1, re.I)

       if "BP1_Name" in Values: # Ersetzung für neues Burklimat
           BP1_Name = re.sub(r".*BP1_Name:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", BP1_Name)
           if match:
               BP1_Name = BP1_Name[:match.start()]
           Values = re.sub("BP1_Name:=(\s*)(.+?)(,)","BP1_Name:='" + BP1_Name + "', ",Values,1, re.I)

       if "BA0_Name" in Values: # Ersetzung für neues Burklimat
           BA0_Name = re.sub(r".*BA0_Name:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", BA0_Name)
           if match:
               BA0_Name = BA0_Name[:match.start()]
           Values = re.sub("BA0_Name:=(\s*)(.+?)(,)","BA0_Name:='" + BA0_Name + "', ",Values,1, re.I)

       if "BA1_Name" in Values: # Ersetzung für neues Burklimat
           BA1_Name = re.sub(r".*BA1_Name:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", BA1_Name)
           if match:
               BA1_Name = BA1_Name[:match.start()]
           Values = re.sub("BA1_Name:=(\s*)(.+?)(,)","BA1_Name:='" + BA1_Name + "', ",Values,1, re.I)
           
       if "BA2_Name" in Values: # Ersetzung für neues Burklimat
           BA2_Name = re.sub(r".*BA2_Name:=","",Values, 2, re.I)
           match = re.search(r"(,|\s)", BA2_Name)
           if match:
               BA2_Name = BA2_Name[:match.start()]
           Values = re.sub("BA2_Name:=(\s*)(.+?)(,)","BA2_Name:='" + BA2_Name + "', ",Values,1, re.I)
            
       if "BA3_Name" in Values: # Ersetzung für neues Burklimat
           BA3_Name = re.sub(r".*BA3_Name:=","",Values, 3, re.I)
           match = re.search(r"(,|\s)", BA3_Name)
           if match:
               BA3_Name = BA3_Name[:match.start()]
           Values = re.sub("BA3_Name:=(\s*)(.+?)(,)","BA3_Name:='" + BA3_Name + "', ",Values,1, re.I)
            
       if "BA4_Name" in Values: # Ersetzung für neues Burklimat
           BA4_Name = re.sub(r".*BA4_Name:=","",Values, 4, re.I)
           match = re.search(r"(,|\s)", BA4_Name)
           if match:
               BA4_Name = BA4_Name[:match.start()]
           Values = re.sub("BA4_Name:=(\s*)(.+?)(,)","BA4_Name:='" + BA4_Name + "', ",Values,1, re.I)
            
       if "BA5_Name" in Values: # Ersetzung für neues Burklimat
           BA5_Name = re.sub(r".*BA5_Name:=","",Values, 5, re.I)
           match = re.search(r"(,|\s)", BA5_Name)
           if match:
               BA5_Name = BA5_Name[:match.start()]
           Values = re.sub("BA5_Name:=(\s*)(.+?)(,)","BA5_Name:='" + BA5_Name + "', ",Values,1, re.I)

       
       
           
       
       WriteLine = "    " + VarList[VarIndex]+ " : " + dictVarType[VarList[VarIndex]] + Values + "; " + dictVarComment.get(VarList[VarIndex],"") + "\n"
       if (ErwAusgabe == "j"):
          print("Variable erstellt: ",WritErwAusgabeeLine)
       fVarOUT.write(WriteLine)
       

       if dictVarComment.get(VarList[VarIndex]) :
           DPzaehlerErstellung += 1

       VarIndex += 1


    fVarOUT.write("\nEND_VAR") 

    print ("Es wurden ",VarIndex," Variablen erzeugt")
    print ("Es wurden ",DPzaehlerErstellung," Burklimat-Datenpunkte erzeugt")

    if (DPzaehler - DPzaehlerErstellung > 0):
       print("\nAchtung: Es sind in der DpList mehr DPs angelegt, als in der ursprünglichen Global.var gefunden wurden!")

    if (GruppeFehlt > 0):
      print("\nAchtung: Nicht alle Datenpunkte waren in der ursprünglichen gruppen.dat enthalten! Siehe Ausgabe oben!")

    fDplistIN.close()
    fGruppenIN.close()
    fVarIN.close()
    fVarOUT.close()


    print("\nKonvertierung abgeschlossen")
    











###########################################################################################################
    

# GUI erstellen
root = tk.Tk()
root.title("Bk2000 zu BkNG Konverter V 1.03")

# Labels + Eingabefelder + Buttons
def create_row(label_text, var_name, row):
    label = tk.Label(root, text=label_text)
    label.grid(row=row, column=0, padx=5, pady=5, sticky="w")

    entry = tk.Entry(root, width=50)
    entry.grid(row=row, column=1, padx=5, pady=5)

    button = tk.Button(root, text="Durchsuchen",
                       command=lambda: select_file(entry, var_name))
    button.grid(row=row, column=2, padx=5, pady=5)

create_row("dplist.dat altes Projekt:", "dp", 0)
create_row("gruppen.dat altes Projekt:", "gruppen", 1)
create_row("Global.var altes Projekt:", "old", 2)
create_row("Global.var neues BkNG-Projekt:", "new", 3)

# Start-Button
start_button = tk.Button(root, text="Start", command=start_conversion, bg="orange", fg="black")
start_button.grid(row=4, column=1, pady=10, padx=10, ipadx=50)


output_text = tk.Text(root, height=15, width=80)
output_text.grid(row=5, column=0, columnspan=3, padx=5, pady=5)


sys.stdout = TextRedirector(output_text)
sys.stderr = TextRedirector(output_text)  # optional für Fehler


root.mainloop()
=======
import tkinter as tk
from tkinter import filedialog
import re
import sys


class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)  # automatisch scrollen

    def flush(self):
        pass  # notwendig für sys.stdout


ErwAusgabe = 0

def select_file(entry, var_name):
    filepath = filedialog.askopenfilename()
    if filepath:
        entry.delete(0, tk.END)
        entry.insert(0, filepath)

        global PathDpList, PathGruppen, PathGlobalOld, PathGlobalNew
        if var_name == "dp":
            PathDpList = filepath
        elif var_name == "gruppen":
            PathGruppen = filepath
        elif var_name == "old":
            PathGlobalOld = filepath
        elif var_name == "new":
            PathGlobalNew = filepath

def start_conversion():

    ersterDPgefunden=0
    GruppeFehlt = 0
    ParString = ""
    PabString = ""
    KtxString = ""
    Gruppenzaehler = 0
    DPzaehler = 0
    Varzaehler = 0
    DPzaehlerErstellung = 0
    bBlockGefunden = 0
    PabBlockIndex = 0
    VisBlockIndex = 0
    VarIndex = 0
    dictGruppen = {"Datenpunkt" : "Gruppe"}
    dictVarType = {"Datenpunkt" : "VarType"}
    dictVarComment= {"Datenpunkt" : "Kommentar"}
    dictDPs = {"Datenpunkt" : "Parameter"}
    dictPabBlock = {"Datentyp":"Blockdef"}
    dictVisBlock = {"Datentyp":"Blockdef"}
    VarList = ["Variable"]
    PabBlockList  = ["Variable"]
    VisBlockList  = ["Variable"]


    print("Starte Konvertierung...")
    print("PathDpList:", PathDpList)
    print("PathGruppen:", PathGruppen)
    print("PathGlobalOld:", PathGlobalOld)
    print("PathGlobalNew:", PathGlobalNew)


###########################################################################################################


   
    fDplistIN = open(PathDpList, "r")
    fGruppenIN = open(PathGruppen, "r")
    fVarIN = open(PathGlobalOld, "r")

    fVarOUT = open(PathGlobalNew, "w")

    # Dictionary für Gruppen erstellen

    if (ErwAusgabe == "j"):
      print("Konvertierung gestartet\n")


    if (ErwAusgabe == "j"):
      print("Global.var aus altem Projekt wird durchsucht\n")


    for lineVar in fVarIN:
       
      if "VAR" not in lineVar and "(*" not in lineVar[:3] and ":" in lineVar:
           VarName = lineVar[:lineVar.find(":")]
           VarName = VarName.strip()
           VarType = lineVar[lineVar.find(":"):lineVar.find(";")]
           VarType = VarType.strip(" : ")
           VarType = VarType.strip()
           dictVarComment[VarName] = lineVar[lineVar.find("(*"):lineVar.find("*)")+2]
           
           #print(VarComment)
           if (ErwAusgabe == "j"):
              print("Variable gefunden: ",VarName," : ",VarType)
           VarList.append(VarName)
           dictVarType[VarName] = VarType

           VarIndex +=1
    print("\nEs wurden ",VarIndex," Variablen gefunden")   


    print("\nGruppen.dat aus altem Projekt wird durchsucht")

    for lineGruppen in fGruppenIN:

       if "$" in lineGruppen:                         #Gruppe gefunden
           aktGruppe = lineGruppen
           aktGruppe = aktGruppe.strip(" \"@,$\n")             #entfernt Whitespace, ", , @, ...
           Gruppenzaehler += 1
           if (ErwAusgabe == "j"):
              print("Gruppe gefunden: ", aktGruppe)

       if "@" in lineGruppen:                         #DP gefunden
           lineGruppen = lineGruppen[2:]  #entfernt Kommentare
           match = re.search(r"(\")", lineGruppen)
           if match:
               lineGruppen = lineGruppen[:match.start()]
           lineGruppen = lineGruppen.strip(" \"@,")            #entfernt Whitespace, ", , @, ...
           dictGruppen[lineGruppen] = aktGruppe

    #print("dictGruppen: ",dictGruppen)
       
    #dictGruppen.update({"UST_Status" : "Unterstationsstatus"})

    print ("\nEs wurden ",Gruppenzaehler," Gruppe(n) gefunden")


    print("\ndplist.dat aus altem Projekt wird durchsucht:")



    for lineDplist in fDplistIN:

    ############################################



       if "$" in lineDplist:                                       #Blockdefinition gefunden
           bBlockGefunden = 1
           BlockTyp = lineDplist[lineDplist.find("$")+1:lineDplist.find("\n")]
           BlockTyp = BlockTyp[:BlockTyp.find("\"")]
           BlockTyp = BlockTyp.strip()
           BlockTyp = BlockTyp.upper()
           if (ErwAusgabe == "j"):
              print("gefundene Blockdefinition: ",BlockTyp)
           
           
           
       if "#PAB" in lineDplist and bBlockGefunden and len(lineDplist)>8:            #PAB gefunden
           #print(len(lineDplist))
           if (ErwAusgabe == "j"):
              print(lineDplist)
           dictPabBlock[BlockTyp] = lineDplist[:lineDplist.find("\n")]
           dictPabBlock[BlockTyp] = dictPabBlock[BlockTyp].removeprefix("\"#PAB")
           dictPabBlock[BlockTyp] = dictPabBlock[BlockTyp][:dictPabBlock[BlockTyp].find("\"")]
           dictPabBlock[BlockTyp] = dictPabBlock[BlockTyp].strip()
           dictPabBlock[BlockTyp] = dictPabBlock[BlockTyp].replace(" ",", ")
           #print("dictPabBlock ",dictPabBlock)


       if "#VIS" in lineDplist and bBlockGefunden:               #VIS gefunden
           if (ErwAusgabe == "j"):
              print(lineDplist)
           dictVisBlock[BlockTyp] = lineDplist[:lineDplist.find(";")]
           dictVisBlock[BlockTyp] = re.sub(r"\"#VIS\s*","",dictVisBlock[BlockTyp], 1, re.I)
           dictVisBlock[BlockTyp] = dictVisBlock[BlockTyp][:dictVisBlock[BlockTyp].find("\"")]
           dictVisBlock[BlockTyp] = dictVisBlock[BlockTyp].strip()
           dictVisBlock[BlockTyp] = dictVisBlock[BlockTyp].replace(" ",", ")
           #print("dictVisBlock ",dictVisBlock)

      

    ##############################################  
       
       
       if "@" in lineDplist and not ";" in lineDplist[:1] :        # Bk-Datenpunkt gefunden
           bBlockGefunden = 0

           dpname = lineDplist[0:lineDplist.find(";")]
           dpname = dpname.replace("\",","")
           dpname = dpname.strip(" @;\" ")
           dpname = dpname.strip()
           if (ErwAusgabe == "j"):
              print("DP Name gefunden: ",dpname)
           if "UST_Status" in dpname:
               dictGruppen.update({dpname : "Unterstationsstatus"})
               
           ersterDPgefunden=1
           if dpname in dictGruppen:
               ParString = " = (Gruppe=\'" +dictGruppen[dpname] + "\')"
               if "UST_Status" in dpname:
                  ParString = " "
           else:
              if "UST_Status" not in dpname:
                 print("Fehler: ->",dpname," - nicht in gruppen.dat!")
                 print("Es wird \"Undefinert\" als Gruppenname verwendet\n")
                 ParString = " = (Gruppe=\'Undefiniert\')"
                 GruppeFehlt = 1
           #print(ParString)       
           dictDPs[dpname] = ParString

           AktDatentyp = dictVarType.get(dpname,"")
           if (ErwAusgabe == "j"):
              print("DP-Typ: ",AktDatentyp)
           AktDatentyp = AktDatentyp.removeprefix("Bk")
           AktDatentyp = AktDatentyp.upper()


           if AktDatentyp in dictPabBlock: #Blockdefinitionen hinzufügen, wenn vorhanden
               ParString = ParString.replace("Gruppe=\'",dictPabBlock[AktDatentyp] + " ,Gruppe=\'")
           #print("ParString nach Blockdef ",ParString)

           if AktDatentyp in dictVisBlock: #Blockdefinitionen hinzufügen, wenn vorhanden
               ParString = ParString.replace("Gruppe=\'",dictVisBlock[AktDatentyp] + " ,Gruppe=\'")
               ParString = re.sub(r"\( ,","(",ParString, 1, re.I)
           #print("ParString nach Blockdef ",ParString)    


           DPzaehler += 1

           
           
       if "~" in lineDplist:                                       #Klartext gefunden
           KtxString = "Klartext='"
           KtxString += lineDplist.strip("~\", ")
           KtxString = KtxString.strip()
           KtxString = KtxString.replace("\",","',")
           KtxString = KtxString.replace(",","")
           #print("KtxString: ",KtxString)
           ParString = ParString.replace("Gruppe=\'",KtxString + ", Gruppe=\'")
           
           dictDPs[dpname] = ParString
           #print("ParString",ParString)

      
       if "#PAB" in lineDplist and ersterDPgefunden and not bBlockGefunden:               #PAB gefunden
           PabString = lineDplist[:lineDplist.find(";")]
           PabString = PabString.removeprefix("\"#PAB")
           PabString = PabString.strip()
           PabString = re.sub(r"\".*","",PabString, 1, re.I)

           PabBlockList = PabString.split() #Aufteilen der Elemente in #PAB
           #print(PabBlockList)
           #print("PabString aus #PAB ",PabString)

           PabBlockIndex = 0
           while PabBlockIndex < len(PabBlockList):
               PabAttribut = PabBlockList[PabBlockIndex]
               PabAttribut = PabAttribut[:PabAttribut.find("=")]
               PabWert = PabBlockList[PabBlockIndex]


               if re.search(PabAttribut, ParString, re.I):
                   #print("Attribut ",PabWert)
                   ParString = re.sub(PabAttribut+"=[^\s,]+",PabWert,ParString, 1, re.I)
                   #print("ParString ",ParString)
               else:
                   ParString = ParString.replace("Gruppe=\'",PabWert + ", Gruppe=\'")

               PabBlockIndex += 1
     
           dictDPs[dpname] = ParString
     

       if "#VIS" in lineDplist and ersterDPgefunden and len(lineDplist)>9 and not bBlockGefunden: #VIS gefunden und VIS nicht leer
           VisString = lineDplist[:lineDplist.find(";")]
           VisString = VisString.removeprefix("\"#VIS")
           VisString = VisString.strip()
           VisString = re.sub(r"\".*","",VisString, 1, re.I)

           VisBlockList = VisString.split() #Aufteilen der Elemente in #VIS
           #print(VisBlockList)
           #print("VisString aus #VIS ",VisString)

           VisBlockIndex = 0
           while VisBlockIndex < len(VisBlockList):
               VisAttribut = VisBlockList[VisBlockIndex]
               VisAttribut = VisAttribut[:VisAttribut.find("=")]
               #VisAttribut = VisAttribut.title()
               VisWert = VisBlockList[VisBlockIndex]
               
               #print(VisAttribut)

               if re.search(VisAttribut, ParString, re.I):
                   #print("Attribut ",VisWert)
                   ParString = re.sub(VisAttribut+"=[^\s,]+",VisWert,ParString, 1, re.I)
                   #print("ParString ",ParString)
               else:
                   ParString = ParString.replace("Gruppe=\'",VisWert + ", Gruppe=\'")

               VisBlockIndex += 1
           #print("ParString nach #VIS ",ParString) 

             

           dictDPs[dpname] = ParString

       
               
    #print(dictDPs)
    print ("\nEs wurden ",DPzaehler," Burklimat-Datenpunkte gefunden")    
       


    print("\nneue Global.var wird erzeugt")


    fVarOUT.write("VAR\n")
    fVarOUT.write("\tVisUstStat : ARRAY[0..7] OF BOOL;\n")

    VarIndex = 1



    while VarIndex < len(VarList) :

       # Ersetzungen
       # Vorlage für Ersetzungen: Values = re.sub(r"SUCHEN","ERSETZEN",Values, 1 ,re.I)

       Values = dictDPs.get(VarList[VarIndex],"")
       #print("vor Umformatierung: ",Values)

       Values = Values.replace("=",":=")
       #Values = Values.replace("'","\"")
       
           
       Values = re.sub(r"(Y|y).(EINH|Einh|einh)","UnitY",Values, 1, re.I)
       Values = re.sub(r"\w*.(EINH|Einh|einh)","Unit",Values, 1, re.I)
       
       if "BkRk" in dictVarType[VarList[VarIndex]]:
          Values = re.sub(r"w.kpos","KposXW",Values, 1, re.I)
          Values = re.sub(r"w.kpos","KposXW",Values, 1, re.I)
          Values = re.sub(r"y.kpos","KposY",Values, 1, re.I)
          
       Values = re.sub(r"\w*.kpos","Kpos",Values, 1, re.I)
       Values = re.sub(r"Hand:=A","Hand:=0",Values, 1, re.I)
       Values = re.sub(r"Int:=I","Int:=1",Values, 1, re.I)
       Values = re.sub(r"Int:=E","Int:=0",Values, 1, re.I)
       Values = re.sub(r"W.MAX","Wmax",Values, 1, re.I)
       Values = re.sub(r"W.MIN","Wmin",Values, 1, re.I)
       Values = re.sub(r"SW.MAX","SWmax",Values, 1, re.I)
       Values = re.sub(r"SW.MIN","SWmin",Values, 1, re.I)
       Values = re.sub(r"Yrmin","YrMin",Values, 1, re.I)
       Values = re.sub(r"Yrmax","YrMax",Values, 1, re.I)
       Values = re.sub(r"SMAX","Smax",Values, 1, re.I)
       Values = re.sub(r"Wert.T0","BP0_Name",Values, 1, re.I)
       Values = re.sub(r"Wert.T1","BP1_Name",Values, 1, re.I)
       Values = re.sub(r"XWG","Xwg",Values, 1, re.I)
       Values = re.sub(r"BAMAX","BAmax",Values, 1, re.I)
       Values = re.sub(r"SWAUT","SWaut",Values, 1, re.I)
       Values = re.sub(r"BA.T0","BA0_Name",Values, 1, re.I)
       Values = re.sub(r"BA.T1","BA1_Name",Values, 1, re.I)
       Values = re.sub(r"BA.T2","BA2_Name",Values, 1, re.I)
       Values = re.sub(r"BA.T3","BA3_Name",Values, 1, re.I)
       Values = re.sub(r"BA.T4","BA4_Name",Values, 1, re.I)
       Values = re.sub(r"Saus.T0","SB0_Name",Values, 1, re.I)
       Values = re.sub(r"Saus.T1","SB1_Name",Values, 1, re.I)
       Values = re.sub(r"Saus.T2","SB2_Name",Values, 1, re.I)
       Values = re.sub(r"Saus.T3","SB3_Name",Values, 1, re.I)
       Values = re.sub(r"Saus.T4","SB4_Name",Values, 1, re.I)
       Values = re.sub(r"RmgSb.T0","SB0_RmName",Values, 1, re.I)
       Values = re.sub(r"RmgSb.T1","SB1_RmName",Values, 1, re.I)
       Values = re.sub(r"RmgSb.T2","SB2_RmName",Values, 1, re.I)
       Values = re.sub(r"RmgSb.T3","SB3_RmName",Values, 1, re.I)
       
       Values = re.sub(r"Rmg.T0","SBX_RmName",Values, 1, re.I)
       Values = re.sub(r"Rmg.T1","SB0_RmName",Values, 1, re.I)
       Values = re.sub(r"Rmg.T2","SB1_RmName",Values, 1, re.I)
       Values = re.sub(r"Rmg.T3","SBY_RmName",Values, 1, re.I)

       Values = re.sub(r"\"","'",Values, 1, re.I)

       
       if "Unit" in Values: # Die Einheit wird extrahiert und in "..." gesetzt
           Einheit = re.sub(r".*Unit:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", Einheit)
           if match:
               Einheit = Einheit[:match.start()]
           Values = re.sub("Unit:=(\s*)(.+?)(,)","Unit:='" + Einheit + "', ",Values,1, re.I)

       if "UnitY" in Values: # Ersetzung für neues Burklimat
           EinheitY = re.sub(r".*UnitY:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", EinheitY)
           if match:
               EinheitY = EinheitY[:match.start()]
           Values = re.sub("UnitY:=(\s*)(.+?)(,)","UnitY:='" + EinheitY + "', ",Values,1, re.I)


       if "SB0_RmName" in Values: # Ersetzung für neues Burklimat
           SB0_RmName = re.sub(r".*SB0_RmName:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", SB0_RmName)
           if match:
               SB0_RmName = SB0_RmName[:match.start()]
           Values = re.sub("SB0_RmName:=(\s*)(.+?)(,)","SB0_RmName:='" + SB0_RmName + "', ",Values,1, re.I)

       if "SB1_RmName" in Values: # Ersetzung für neues Burklimat
           SB1_RmName = re.sub(r".*SB1_RmName:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", SB1_RmName)
           if match:
               SB1_RmName = SB1_RmName[:match.start()]
           Values = re.sub("SB1_RmName:=(\s*)(.+?)(,)","SB1_RmName:='" + SB1_RmName + "', ",Values,1, re.I)

       if "SB2_RmName" in Values: # Ersetzung für neues Burklimat
           SB2_RmName = re.sub(r".*SB2_RmName:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", SB2_RmName)
           if match:
               SB2_RmName = SB2_RmName[:match.start()]
           Values = re.sub("SB2_RmName:=(\s*)(.+?)(,)","SB2_RmName:='" + SB2_RmName + "', ",Values,1, re.I)

       if "SB3_RmName" in Values: # Ersetzung für neues Burklimat
           SB3_RmName = re.sub(r".*SB3_RmName:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", SB3_RmName)
           if match:
               SB3_RmName = SB3_RmName[:match.start()]
           Values = re.sub("SB3_RmName:=(\s*)(.+?)(,)","SB3_RmName:='" + SB3_RmName + "', ",Values,1, re.I)

       if "SB4_RmName" in Values: # Ersetzung für neues Burklimat
           SB4_RmName = re.sub(r".*SB4_RmName:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", SB4_RmName)
           if match:
               SB4_RmName = SB4_RmName[:match.start()]
           Values = r("SB4_RmName:=(\s*)(.+?)(,)","SB4_RmName:='" + SB4_RmName + "', ",Values,1, re.I)

       if "SBX_RmName" in Values: # Ersetzung für neues Burklimat
           SBX_RmName = re.sub(r".*SBX_RmName:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", SBX_RmName)
           if match:
               SBX_RmName = SBX_RmName[:match.start()]
           Values = re.sub("SBX_RmName:=(\s*)(.+?)(,)","SBX_RmName:='" + SBX_RmName + "', ",Values,1, re.I)

       if "SBY_RmName" in Values: # Ersetzung für neues Burklimat
           SBY_RmName = re.sub(r".*SBY_RmName:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", SBY_RmName)
           if match:
               SBY_RmName = SBY_RmName[:match.start()]
           Values = re.sub("SBY_RmName:=(\s*)(.+?)(,)","SBY_RmName:='" + SBY_RmName + "', ",Values,1, re.I)

           

       if "SB0_Name" in Values: # Ersetzung für neues Burklimat
           SB0_Name = re.sub(r".*SB0_Name:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", SB0_Name)
           if match:
               SB0_Name = SB0_Name[:match.start()]
           Values = re.sub("SB0_Name:=(\s*)(.+?)(,)","SB0_Name:='" + SB0_Name + "', ",Values,1, re.I)

       if "SB1_Name" in Values: # Ersetzung für neues Burklimat
           SB1_Name = re.sub(r".*SB1_Name:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", SB1_Name)
           if match:
               SB1_Name = SB1_Name[:match.start()]
           Values = re.sub("SB1_Name:=(\s*)(.+?)(,)","SB1_Name:='" + SB1_Name + "', ",Values,1, re.I)

       if "SB2_Name" in Values: # Ersetzung für neues Burklimat
           SB2_Name = re.sub(r".*SB2_Name:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", SB2_Name)
           if match:
               SB2_Name = SB2_Name[:match.start()]
           Values = re.sub("SB2_Name:=(\s*)(.+?)(,)","SB2_Name:='" + SB2_Name + "', ",Values,1, re.I)
           
       if "SB3_Name" in Values: # Ersetzung für neues Burklimat
           SB3_Name = re.sub(r".*SB3_Name:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", SB3_Name)
           if match:
               SB3_Name = SB3_Name[:match.start()]
           Values = re.sub("SB3_Name:=(\s*)(.+?)(,)","SB3_Name:='" + SB3_Name + "', ",Values,1, re.I)
           
       if "SB4_Name" in Values: # Ersetzung für neues Burklimat
           SB4_Name = re.sub(r".*SB4_Name:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", SB4_Name)
           if match:
               SB4_Name = SB4_Name[:match.start()]
           Values = re.sub("SB4_Name:=(\s*)(.+?)(,)","SB4_Name:='" + SB4_Name + "', ",Values,1, re.I)

       if "BP0_Name" in Values: # Ersetzung für neues Burklimat
           BP0_Name = re.sub(r".*BP0_Name:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", BP0_Name)
           if match:
               BP0_Name = BP0_Name[:match.start()]
           Values = re.sub("BP0_Name:=(\s*)(.+?)(,)","BP0_Name:='" + BP0_Name + "', ",Values,1, re.I)

       if "BP1_Name" in Values: # Ersetzung für neues Burklimat
           BP1_Name = re.sub(r".*BP1_Name:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", BP1_Name)
           if match:
               BP1_Name = BP1_Name[:match.start()]
           Values = re.sub("BP1_Name:=(\s*)(.+?)(,)","BP1_Name:='" + BP1_Name + "', ",Values,1, re.I)

       if "BA0_Name" in Values: # Ersetzung für neues Burklimat
           BA0_Name = re.sub(r".*BA0_Name:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", BA0_Name)
           if match:
               BA0_Name = BA0_Name[:match.start()]
           Values = re.sub("BA0_Name:=(\s*)(.+?)(,)","BA0_Name:='" + BA0_Name + "', ",Values,1, re.I)

       if "BA1_Name" in Values: # Ersetzung für neues Burklimat
           BA1_Name = re.sub(r".*BA1_Name:=","",Values, 1, re.I)
           match = re.search(r"(,|\s)", BA1_Name)
           if match:
               BA1_Name = BA1_Name[:match.start()]
           Values = re.sub("BA1_Name:=(\s*)(.+?)(,)","BA1_Name:='" + BA1_Name + "', ",Values,1, re.I)
           
       if "BA2_Name" in Values: # Ersetzung für neues Burklimat
           BA2_Name = re.sub(r".*BA2_Name:=","",Values, 2, re.I)
           match = re.search(r"(,|\s)", BA2_Name)
           if match:
               BA2_Name = BA2_Name[:match.start()]
           Values = re.sub("BA2_Name:=(\s*)(.+?)(,)","BA2_Name:='" + BA2_Name + "', ",Values,1, re.I)
            
       if "BA3_Name" in Values: # Ersetzung für neues Burklimat
           BA3_Name = re.sub(r".*BA3_Name:=","",Values, 3, re.I)
           match = re.search(r"(,|\s)", BA3_Name)
           if match:
               BA3_Name = BA3_Name[:match.start()]
           Values = re.sub("BA3_Name:=(\s*)(.+?)(,)","BA3_Name:='" + BA3_Name + "', ",Values,1, re.I)
            
       if "BA4_Name" in Values: # Ersetzung für neues Burklimat
           BA4_Name = re.sub(r".*BA4_Name:=","",Values, 4, re.I)
           match = re.search(r"(,|\s)", BA4_Name)
           if match:
               BA4_Name = BA4_Name[:match.start()]
           Values = re.sub("BA4_Name:=(\s*)(.+?)(,)","BA4_Name:='" + BA4_Name + "', ",Values,1, re.I)
            
       if "BA5_Name" in Values: # Ersetzung für neues Burklimat
           BA5_Name = re.sub(r".*BA5_Name:=","",Values, 5, re.I)
           match = re.search(r"(,|\s)", BA5_Name)
           if match:
               BA5_Name = BA5_Name[:match.start()]
           Values = re.sub("BA5_Name:=(\s*)(.+?)(,)","BA5_Name:='" + BA5_Name + "', ",Values,1, re.I)

       
       
           
       
       WriteLine = "    " + VarList[VarIndex]+ " : " + dictVarType[VarList[VarIndex]] + Values + "; " + dictVarComment.get(VarList[VarIndex],"") + "\n"
       if (ErwAusgabe == "j"):
          print("Variable erstellt: ",WritErwAusgabeeLine)
       fVarOUT.write(WriteLine)
       

       if dictVarComment.get(VarList[VarIndex]) :
           DPzaehlerErstellung += 1

       VarIndex += 1


    fVarOUT.write("\nEND_VAR") 

    print ("Es wurden ",VarIndex," Variablen erzeugt")
    print ("Es wurden ",DPzaehlerErstellung," Burklimat-Datenpunkte erzeugt")

    if (DPzaehler - DPzaehlerErstellung > 0):
       print("\nAchtung: Es sind in der DpList mehr DPs angelegt, als in der ursprünglichen Global.var gefunden wurden!")

    if (GruppeFehlt > 0):
      print("\nAchtung: Nicht alle Datenpunkte waren in der ursprünglichen gruppen.dat enthalten! Siehe Ausgabe oben!")

    fDplistIN.close()
    fGruppenIN.close()
    fVarIN.close()
    fVarOUT.close()


    print("\nKonvertierung abgeschlossen")
    











###########################################################################################################
    

# GUI erstellen
root = tk.Tk()
root.title("Bk2000 zu BkNG Konverter V 1.03")

# Labels + Eingabefelder + Buttons
def create_row(label_text, var_name, row):
    label = tk.Label(root, text=label_text)
    label.grid(row=row, column=0, padx=5, pady=5, sticky="w")

    entry = tk.Entry(root, width=50)
    entry.grid(row=row, column=1, padx=5, pady=5)

    button = tk.Button(root, text="Durchsuchen",
                       command=lambda: select_file(entry, var_name))
    button.grid(row=row, column=2, padx=5, pady=5)

create_row("dplist.dat altes Projekt:", "dp", 0)
create_row("gruppen.dat altes Projekt:", "gruppen", 1)
create_row("Global.var altes Projekt:", "old", 2)
create_row("Global.var neues BkNG-Projekt:", "new", 3)

# Start-Button
start_button = tk.Button(root, text="Start", command=start_conversion, bg="orange", fg="black")
start_button.grid(row=4, column=1, pady=10, padx=10, ipadx=50)


output_text = tk.Text(root, height=15, width=80)
output_text.grid(row=5, column=0, columnspan=3, padx=5, pady=5)


sys.stdout = TextRedirector(output_text)
sys.stderr = TextRedirector(output_text)  # optional für Fehler


root.mainloop()
>>>>>>> 37a4467b97584275e801e1109ad771400751b701
