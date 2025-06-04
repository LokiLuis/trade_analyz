
#codice principale+cose necessarie per collegamento a render

from flask import Flask, request, jsonify

app = Flask(__name__)

#dcasoftware
#dca+csv
 

def analizza_trade(entrata, rischio_massimo, riskreward_target,coppia_valutaria="EURUSD", allocazioni_dca=(0.10, 0.35, 0.55)):



    

    
    def calcola_valore_per_pip(coppia_valutaria, entrata):
        if "JPY" in coppia_valutaria:
            return (0.01 / entrata) * 100000
        elif coppia_valutaria.upper() == "XAUUSD":
            return 1  # XAUUSD: 0.1 = 1 pip, ogni pip = 1 USD
        else:
            return 10  # Valore standard
        



    valore_per_pip = valore_per_pip = calcola_valore_per_pip(coppia_valutaria, entrata)




    prezzo_stoploss = entrata-(tradingview_Stoploss_in_punti*0.00001)
    
    
    pips_stoploss = int ( tradingview_Stoploss_in_punti / 10 )
    
    
    pips_takeprofit = pips_stoploss * riskreward_target
    
     
    prezzo_takeprofit = entrata + ( pips_stoploss * riskreward_target/ 10000)
    



    # Convertiamo tutto in pips (1 pip = 0.0001)
    pips_stoploss = (entrata - prezzo_stoploss) * 10000  # Differenza in pips
    distanza_tp_pips = (prezzo_takeprofit - entrata) * 10000  # Differenza in pips
    
     


    # Calcoliamo i livelli DCA in pips
    pips_dca1 = pips_stoploss * 1/3
    pips_dca2 = pips_stoploss * 2/3
    
    

    # Prezzi DCA
    prezzo_dca1 = entrata - (pips_dca1 / 10000)
    prezzo_dca2 = entrata - (pips_dca2 / 10000)

    entrate = (entrata, round(prezzo_dca1,5), round(prezzo_dca2,5))

    


    #CALCOLA RiskToReward
    #_____________________


    def calcola_riskreward(prezzo_entrata, prezzo_stoploss, prezzo_takeprofit):
        tp_pips = abs(prezzo_takeprofit - prezzo_entrata) * 10000
        sl_pips = abs(prezzo_entrata - prezzo_stoploss) * 10000
        return tp_pips / sl_pips


    rr_entry = calcola_riskreward(entrata, prezzo_stoploss, prezzo_takeprofit)
    rr_dca1  = calcola_riskreward(prezzo_dca1, prezzo_stoploss, prezzo_takeprofit)
    rr_dca2  = calcola_riskreward(prezzo_dca2, prezzo_stoploss, prezzo_takeprofit)




    # Stampa risultati
    print(f"\n\n{' PARAMETRI TRADE ':-^60}")


     #ordine buy o sell?
    if pips_takeprofit < 0:
        print("\n🔴 SELL")
    else:
        print("\n🟢 BUY>")


    print(f"\nEntry: {entrata:.5f}    DCA1: {prezzo_dca1:.5f}    DCA2: {prezzo_dca2:.5f}\n\n")
    print(f"SL: {prezzo_stoploss:.5f} (Rischio: {pips_stoploss:.0f} pips)")
    print(f"\nTP: {prezzo_takeprofit:.5f} (Target: {distanza_tp_pips:.0f} pips)")





    #Calcolo lotti dopo aver inserito stoploss pips
    print(f"\n\n\n{' GESTIONE LOTTI ':-^60}\n")

    messaggi_entrate = ("entry","dca1","dca2" )
    lotti = []
    allocazioni_dca = (0.10, 0.35, 0.55)

    for i in range(3):  # 0, 1, 2 per allocazioni[0], [1], [2]
        lotto = (rischio_massimo * allocazioni_dca[i] ) / (pips_stoploss * 10) ########
        lotto_arrotondato = round(lotto, 3)
        lotti.append(lotto_arrotondato)
        print( messaggi_entrate[i],lotto_arrotondato,"LOTTI","     (price)",entrate[i] )  # Stampa ogni risultato

    


    guadagni = []

    for i in range(3):
        pips = (prezzo_takeprofit - entrate[i]) * 10000
        guadagno = pips * valore_per_pip * lotti[i]
        guadagni.append(guadagno)
        #print(f"Guadagno {messaggi_entrate[i]}: {guadagno:.2f} USD")      #messaggio ulteriore che gia abbiamo riguardo i guadagni
    
    

    perdite = []

    for i in range(3):
        pips = abs(entrate[i] - prezzo_stoploss) * 10000
        perdita = pips * valore_per_pip * lotti[i]
        perdite.append(perdita)
        #print(f"Perdita trade {i+1}: {round(perdita,2)} €")  # 3 print differenti riguardo perdite dei 3 trade

    
    
    
    
    
    print(f"\n\n{' RISULTATI ':-^60}")
    print(f"\n✅ Entry: +{guadagni[0]:.2f}€        (-{ rischio_massimo * allocazioni_dca[0]:.0f}€)         📈 R:R  {round(rr_entry, 2)}" )
    print(f"\n✅ Dca1: +{guadagni[1]:.2f}€        (-{round(perdite[1],2)}€)      📈 R:R  {round(rr_dca1,2)}" )
    print(f"\n✅ Dca2: +{guadagni[2]:.2f}€       (-{round(perdite[2],2)}€)      📈 R:R  {round(rr_dca2, 2)}" )
    print(f"\n\n❌ Stop Loss: -{round(sum(perdite),2)}€")
    print("\n✅ Guadagno Totale:", round((guadagni[0] + guadagni[1] + guadagni[2]),2),"€")
    


    print(f"\n\n\n{' ALLOCAZIONI ':-^60}")
    print(f"\n({allocazioni_dca[0]*100:.0f}%) Entry:  {round(rischio_massimo * allocazioni_dca[0], 1)}€         ({allocazioni_dca[1]*100:.0f}%) Dca1:  {round(rischio_massimo * allocazioni_dca[1], 1)}€         ({allocazioni_dca[2]*100:.0f}%) Dca2:  {round(rischio_massimo * allocazioni_dca[2], 1)}€")
    print(f"\nValore per pip ({coppia_valutaria.upper()}):  {valore_per_pip:.2f}€\n____________________________")





   
    


    
    # INSERISCI DATI PER ELABORARE

#entry =  1.02

#tradingview_Stoploss_in_punti =  -500  #  in pips da vista tradingview, guardando lo strmento per disegnare trade

##rischio_massimo =  100    #  1% del capitale

##riskreward_target =  2

#coppia_valutaria = "USDJPY"   # <--- (usa le " " , cambia in base alla coppia che stai tradando

#coppia_valutaria = "EURUSD"

#coppia_valutaria = "XAUUSD"

#analizza_trade(entry, rischio_massimo, riskreward_target,coppia_valutaria)


@app.route("/", methods=["GET"])
def home():
    return "✅ API online!"

@app.route("/calcola", methods=["POST"])
def calcola():
    data = request.get_json()

    entry = float(data.get("entry"))
    rischio_massimo = float(data.get("rischio_massimo"))
    riskreward_target = float(data.get("riskreward_target"))
    coppia_valutaria = data.get("coppia_valutaria", "EURUSD")
    global tradingview_Stoploss_in_punti
    tradingview_Stoploss_in_punti = int(data.get("tradingview_Stoploss_in_punti"))

    # Chiama la funzione esistente
    analizza_trade(entry, rischio_massimo, riskreward_target, coppia_valutaria)
    
    return jsonify({"status": "successo", "msg": "Analisi completata."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
