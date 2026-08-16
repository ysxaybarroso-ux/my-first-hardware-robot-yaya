import time 
import perception.stt
import core.config
import core.servo_controller
import behavior.state_machine
import perception.connectivite
import perception.stt
import behavior.api_gemini
import behavior.tts 
import behavior.llm_local as llm

dernier_appel = 0
state = "no order"
commande_found = None
reponse = "" 

def Traiter_commande():
    global state ,commande_found, reponse 
    global dernier_appel
    while True:
        texte = perception.stt.texte
        new_texte =texte.split()
        commande_found = False
        for mot in new_texte:
            if mot == "nessie":
                dernier_appel = time.time()
        if time.time() - dernier_appel <= 15:

            if "tortue" in new_texte:
                behavior.state_machine.mode_turtle = True
            elif "turtle" in new_texte:
                behavior.state_machine.mode_turtle = True
            elif "normal" in new_texte:
                behavior.state_machine.mode_turtle = False
            else:
                for i, mot in enumerate(new_texte):
                    if mot in core.config.states_vocaux:
                        behavior.state_machine.state = core.config.states_vocaux[mot]
                        break
                    elif new_texte[i] in core.config.directions:
                        behavior.state_machine.state = "ORDER"
                        commande_found = True
                        behavior.state_machine.direction = core.config.directions[new_texte[i]]
                        if i + 1 < len(new_texte) and  (new_texte[i+1] in ["peu", "un"] or new_texte[i+1] in ["a","little"]):
                            core.servo_controller.objectif_pas = 4
                        elif i + 1 < len(new_texte) and  (new_texte[i+1] == "beaucoup" or new_texte[i+1] in ["far","away"]):
                            core.servo_controller.objectif_pas = 8
                        else : 
                            core.servo_controller.objectif_pas = 6

            if commande_found == False:
                if perception.connectivite.isConnected == True:
                    behavior.state_machine.isTalking = True
                    reponse = behavior.api_gemini.demander_api(texte)
                    behavior.tts.vocal(reponse)
                    behavior.state_machine.isTalking = False
                else:
                    behavior.state_machine.isTalking = True
                    reponse = llm.demander_llm(texte)
                    behavior.tts.vocal(reponse)
                    behavior.state_machine.isTalking = False
        

