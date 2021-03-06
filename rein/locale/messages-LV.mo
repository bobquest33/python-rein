��    .      �  =   �      �  r  �  `  d  )   �  
   �     �  
   	  '   	     B	     R	     k	     �	     �	     �	     �	  9   �	     �	     
     "
     4
  U  T
     �     �     �     �     �     �  
             +     9  
   Q     \     n     �     �     �     �     �     �     �          $     <     O     [  C  b  �  �  x  I  0   �     �     �          *     I     a  (   |     �     �     �     �  B   �          ,     L  %   _  ;  �     �     �     �     �                    ,     J     [     {     �     �     �  	   �     �     �          *     H     f     y     �     �  
   �                     $       (          ,             "   	         
                     +       %                 *   #                   )      &   .   -      !                  '                                    
    Rein is a decentralized professional services market and Python-rein is a client
that provides a user interface. Use this program from your local browser or command 
line to create an account, post a job, bid, etc.


    Quick start:
        $ rein start     - create an identity, run the Web UI
        $ rein buy       - request microhosting
        $ rein sync      - push your identity to microhosting servers
        $ rein status    - get user status, or dump of job's documents


    Workers
        $ rein bid       - view and bid on jobs
        $ rein deliver   - complete job by providing deliverables


    Disputes
        $ rein workerdispute    - worker files dispute
        $ rein creatordispute   - job creator files dispute
        $ rein resolve          - mediator posts decision

    For more info and the setup guide visit: http://reinproject.org
     
    Setup or import an identity.

    You will choose a name or handle for your account, include public contact information, 
    and a delegate Bitcoin address/private key that the program will use to sign documents
    on your behalf. An enrollment document will be created and you will need to sign it
    with your master Bitcoin private key.
     1 - Create new account
2 - Import backup
 Bid amount Choose Job to bid on Choose bid Choose job associated with deliverables Choose mediator Delegate Bitcoin address Delegate Bitcoin private Key Deliverables Description Dispute detail Disputes Do you want to import a backup or create a new account?

 Email / Bitmessage Error connecting to server. Expiration (days) File containing signed document Funds for each job in Rein are stored in two multisig addresses. One address
is for the primary payment that will go to the worker on completion. The
second address pays the mediator to be available to resolve a dispute
if necessary. The second address should be funded according to the percentage
specified by the mediator and is in addition to the primary payment. The
listing below shows available mediators and the fee they charge. You should
consider the fee as well as any reputational data you are able to find when
choosing a mediator. Your choice may affect the number and quality of bids Invalid address Invalid signature Job name Master Bitcoin address Mediator Fee Name / Handle None found Not a valid private key. Please enter  Register as a mediator? Resolution Signed enrollment Signed mediator payment Signed primary payment Tags Verifying block times... Welcome to Rein. bid submitted complete, dispute resolved complete, work accepted deliverables submitted disputed by job creator disputed by worker job awarded posted Project-Id-Version: 0.2
POT-Creation-Date: 2016-12-21 11:00+PST
PO-Revision-Date: 2017-02-16 19:43+0100
Last-Translator: Kaspars Lapiņš <neeo33@inbox.lv>
Language-Team: Latviešu <LL@li.org>
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Language: lv
X-Generator: Poedit 1.8.11
 
    Rein ir centralizēts pakalpojumu tirgus un Python-rein ir klients
kas nodrošina lietotāja interfeisu. Izmanto šo programmu no jūsu patstāvīgās pārlukprogrammas 
vieta kur reģistrēties, pievono darbu, liec likmes, u.c.


    Ātrā palaišana:
        $ rein start     - izveidot identitāti, palaist tīklu UI
        $ rein buy       - pieprasīt microhostingu
        $ rein sync      - ielikt savu identitāti microhosting serveros
        $ rein status    - dabūt lietotāja statusus, vai kaudzi ar darba doukumentiem


    Darbinieki
        $ rein bid       - apskatīt un ievietot darbus
        $ rein deliver   - pabeigt darbu nodrošinot nodevas


    Strīdi
        $ rein workerdispute    - darbinieku failu apstrīde
        $ rein creatordispute   - darba devēju failu apstrīde
        $ rein resolve          - starpnieks pasludina lēmumu

    Vairāk info šeit: http://reinproject.org
     
    izveidot vai ievietot identitāti.

    Jūs izvēlēsieties savu vārdu priekš jūsu profila, ievietojot publisku kontaktinformāciju, 
    ievietojot Bitcoin adresi/privāto atslēgu ko programma izmantos parakstot dokumentus
    jūsu vārdā. Uzņemšanas dokuments tiks izveidots un jums tas būs jāparaksta
    ar jūsu Bitcoin private key/privāto atslēgu.
     1 - Izveidot profilu
2 - atgūt dublētos datus
 Pieteikties Izvēlēties darbu Izvēlēties pieteikumu Izvēlēties darbu ar nodevām Izvēlēties starpnieku Pārskatīt BITCOIN adresi Pārskatīt Bitcoin Private Key/atslēgu Nodevas Apraksts apstrīdēt detaļas Strīdi Vai vēlaties atgūt dublētos datus vai izveidot jaunu profilu?

 E-pasts / Bitvēstule Kļuda piekļūšanai serverim. Atlikušās dienas Failā ietilpst parakstīts dokuments Uzkrājumi darbā Rein ir saglabāti divās adresēs. Viena adrese
ir priekš primārās samaksas darbiniekam par pabeigtu darbu.
Otrā adrese ir priekš starpnieka, lai varētu atrisināt strīdus
ja vajadzīgs. Otrā adrese tiks uzkrāta ņemot vērā attiecīgos procentus
,to noteiks starpnieks arī ņemot vērā primāro samaksu. The
Saraksts lejā norāda brīvos starpniekus un to procentus ko viņi pieprasa. Jums vajadzētu
apsvērt samaksu starpniekam kā reputācijas datu kad
izvēlēsieties starpnieku. Jūsu izvēle nosaka skaitu un kvalitāti pieteikumiem Nederīga adrese Nederīgs paraksts Darba nosaukums Bitcoin adrese Starnieka samaksa Vārds Netika atrasts nederīga privātā atslēga. Lūdzu ievadiet  Reģistrēties kā starpniekam? Rezolūcija Parakstīta uzņemšana Parakstīta starpnieka samaksa Parakstīta primārā samaksa Etiķetes Pārbauda bloku laiku... Sveicināti Rein. pieteikums apstiprināts Pabeigts, strīds atrisināts Pabeigts, darbs apstiprināts nodevas pieņemtas apstrīdēts no darba devēja apstrīdēts no darbinieka Darbs piešķirts Publicēts 