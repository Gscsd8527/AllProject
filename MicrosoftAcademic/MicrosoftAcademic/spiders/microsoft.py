# -*- coding: utf-8 -*-
import scrapy
import json
import requests
from MicrosoftAcademic.items import MicrosoftacademicItem
import logging

class MicrosoftSpider(scrapy.Spider):
    name = 'microsoft'
    allowed_domains = ['https://academic.microsoft.com']
    start_urls = ['http://https://academic.microsoft.com/']

    def __init__(self):
        # self.KeyWord = ["Psychology", "Political science", "Mathematics", "Environmental science", "Computer science",
        #                 "Medicine", "Biology", "History", "Physics", "Geology", "Engineering", "Philosophy", "Art",
        #                 "Sociology", "Business", "Economics", "Chemistry", "Materials science", "Geography"]
        # self.KeyWord = ["Visual modularity", ]
        self.KeyWord = ["Piaget's theory", 'Infant cognitive development', "Baddeley's model of working memory", 'Articulatory suppression', 'Modality effect', 'Memory rehearsal', 'Brown–Peterson task', 'Redintegration', 'Intermediate-term memory', 'Atkinson–Shiffrin memory model', 'Shortterm Memory', 'Medium-term memory', 'Short-term memory performance', 'Short-term memory test', 'Poor short-term memory', 'Subvocalization', 'Iconic memory', 'Retrospective memory', 'Cambridge Neuropsychological Test Automated Battery', 'Neuroanatomy of memory', 'Exceptional memory', 'Source amnesia', 'Hopkins Verbal Learning Test Revised', 'Corsi block-tapping test', 'Methods used to study memory', 'Memory and social interactions', 'Eyewitness memory (child testimony)', 'Reading span task', 'Symbol Search', 'Digit span performance', 'WAIS-IV Digit Span', 'Digit span forwards', 'Proactive Inhibition', 'Left brain interpreter', 'Write-only memory (joke)', 'Visual short-term memory performance', 'Visual short-term memory task', 'Neural processing for individual categories of objects', 'Self-reference effect', 'Global Executive Composite', 'Metacognition Index', 'Temporal dynamics of music and language', 'Positive affectivity', 'Surgency', 'Impact bias', 'Aprosodias', 'Two-factor theory of emotion', 'Evolution of emotion', 'Discrete emotion theory', 'Warranting theory', 'Neurolaw', 'Positive Neuroscience', 'Augmented cognition', 'Cognitive miser', 'Cold cognition', 'Relapse/recurrence', 'CPT protocol', 'Wechsler Preschool and Primary Scale of Intelligence', 'Wechsler Adult Intelligence Scale-Revised', 'Performance intelligence quotient', 'Wechsler Adult Intelligence Scale - Fourth Edition', 'Wechsler Adult Intelligence Scale IV', 'IQ classification', 'P600', 'Early left anterior negativity', 'Category test', 'Halstead-Reitan Neuropsychological Battery', 'Test of Memory Malingering', 'Symptom validity test', 'Halstead-Reitan battery', 'Speech Sounds Perception Test', 'California Verbal Learning Test - Second Edition', 'Tactual Performance Test', 'Seashore Rhythm Test', 'Multilingual aphasia examination', 'Logical Memory II', 'Logical Memory I', 'NEPSY', 'Neuropsychological diagnosis', 'Wechsler Memory Scale - Fourth Edition', 'The Boston process approach', 'Controlled Oral Word Association Test', 'Controlled Oral Word Association', 'Thurstone Word Fluency Test', 'Modified card sorting test', 'WCST - Wisconsin card sorting test', 'Modified Wisconsin Card Sorting Test', 'Stroop neuropsychological screening test', 'Mental chronometry', 'Cognitive neuropsychiatry', 'Number Cancellation', 'Luria-Nebraska neuropsychological battery', 'Emergent materialism', 'Mind extension', 'Boundaries of the mind', 'Interactionism (philosophy of mind)', 'Intelligibility (philosophy)', 'Reconstructive memory', 'Indirect tests of memory', 'Difference due to memory', 'Childhood amnesia', 'Autonoetic consciousness', 'Time-Based Prospective Memory', "Children's Memory Scale", 'Autobiographical memory interview', 'Selective amnesia', 'Rhinal cortex', 'Postrhinal cortex', 'California Verbal Learning Test II', 'Short Delay Free Recall', 'Context-dependent memory', 'Recognition failure of recallable words', 'Biased Competition Theory', 'Visual modularity', 'Worked-example effect', '5-Choice Serial Reaction Time Task', 'Diagonal sulcus', 'Beuren syndrome', 'GTF2I gene', 'Overfriendliness', 'Mental model theory of reasoning', 'AV Reentrant Tachycardia', 'Antidromic impulse', 'Temporalis tendon', 'Tactual discrimination', 'Riddoch syndrome', 'Riddoch phenomenon', 'Eye movement in reading', 'Speech Reception Threshold Test', 'Structural information theory', 'Deaf-Blind Disorders', 'TRACE (psycholinguistics)', 'Auditory phonetics', 'Speech shadowing', 'Superior temporal area', 'Peripheral drift illusion', 'Stereopsis recovery', 'Cyclodisparity', 'Associative visual agnosia', 'Integrative agnosia', 'Beat deafness', 'Helmholtz pitch notation', 'Theridion californicum', 'Extinction (psychology)', 'Fear-potentiated startle', 'Conditioned emotional response', 'Freezing behavior', 'Second-order conditioning', 'Dorsal premammillary nucleus', 'Extinction therapy', 'Abnormal fear', 'Measures of conditioned emotional response', 'Fear processing in the brain', 'Neurologic Models', 'Kindling model', 'Withdrawal seizures', 'Seizures withdrawal', 'Kindling mechanism', 'Generalized clonic seizures', 'Alcohol withdrawals', 'Anterior olfactory nucleus', 'Association fiber', 'Primary olfactory cortex', 'Olfactory peduncle', 'Tenia tecta', 'Triangular Septal Nucleus', 'Septofimbrial Nucleus', 'Dorsal Septal Nucleus', 'Extended amygdala', 'Medial amygdaloid nucleus', 'Nucleus circularis', 'Premammillary nucleus', 'Dorsal hypothalamic area', 'Central amygdalar nucleus', 'Ventral premammillary nucleus', 'Amygdalohippocampal area', 'Amygdalofugal pathway', 'Anterior Commissural Nucleus', 'Nucleus preopticus medialis', 'Estrogen Receptor Antibody', 'Lateral preoptic nucleus', 'Medial amygdalar nucleus', 'Sublenticular extended amygdala', 'Ansa peduncularis', 'Basomedial amygdaloid nucleus', 'Nucleus interstitialis', 'Paralaminar Nucleus', 'Disks Large Homolog 4 Protein', 'Postsynaptic density proteins', 'HOMER1', 'SHANK2', 'SHANK3 Gene', 'Presynaptic specialization', 'Presynaptic grid', 'Presynaptic density', 'Caldendrin', 'Subsynaptic reticulum', 'Postsynaptic specialization', 'Postsynaptic cytoskeleton', 'Glutamatergic postsynaptic density', 'Neuronal postsynaptic density', 'Genes to Cognition Project', 'Graded potential', 'Homeostatic plasticity', 'Synaptic scaling', 'Synaptic tagging', 'Heterosynaptic plasticity', 'Anti-Hebbian learning', 'BCM theory', 'Homosynaptic plasticity', 'Synaptic pharmacology', 'Nonsynaptic plasticity', 'Neuronal memory allocation', 'Dendritic spine apparatus', 'Dendritic spine head', 'Spine neck', 'Dendritic filopodium', 'Perforant Pathway', 'Trisynaptic circuit', 'Subicular complex', 'Parasubiculum', 'Prosubiculum', 'Postcommissural fornix', 'Hippocampus proper', 'Anteromedial thalamic nucleus', 'Nifene', 'Left subiculum', 'Right subiculum', 'SUBCORTICAL BAND HETEROTOPIA', 'Double Cortex Syndrome', 'Immature neuron', 'Neuroblast differentiation', 'SUBCORTICAL LAMINAR HETEROTOPIA', 'Doublecortin protein', 'Type 1 Lissencephaly', 'Neuronal lineage marker', 'Basal dendrite', 'Lugaro cell', 'Martinotti cell', 'Pericellular basket', 'Golgi I', 'Periallocortex', 'Nucleus Basalis Magnocellularis', 'Diagonal band nucleus', 'Islands of Calleja', 'Cortical amygdaloid nucleus', 'Pars Externa', 'Right olfactory bulb', 'SCH-23390', 'Eticlopride', 'Dihydrexidine', 'Cholecystokinin B receptor', 'L-745,870', 'A-77636', 'Dopamine receptor binding', 'A-68930', 'D2-like receptor', 'Ecopipam', 'D1-like receptor', 'GHB receptor', 'Dopamine Receptor Interactions', 'A-86929', 'Stephania intermedia', 'Dinapsoline', 'Dopamine D2S receptor', 'Endogenous agonist', 'Doxanthrine', 'Dopamine Receptor D1 Gene', 'Dopamine receptor D5', 'Cholecystokinin Type B Receptor', 'Dinoxyline', 'D2 Receptor Antagonist', 'CCKBR Gene', 'Dopamine Receptor Family', 'Epigenetics of cocaine addiction', '7-OH-DPAT', 'Quinelorane', 'Nafadotride', 'Cariprazine', 'BP-897', 'UH-232', 'Iodosulpride', 'PD-128,907', 'Sultopride', 'Oxiperomide', 'Mezilamine', 'Nemonapride', 'N-Methylspiperone', 'Quinpirole Hydrochloride', 'Piflutixol', 'Neuroleptic receptors', '5-hydroxytryptamine binding', 'Spirodecanone', 'Fenoldopam Mesylate', 'BioSocieties', 'Glutamate hypothesis of schizophrenia', 'CY-208,243', 'Trace amine associated receptor 1', 'EPPTB', 'TAAR5', 'TAAR8', 'TAAR2', 'TAAR1 gene', 'RO5166017', 'Mammillary peduncle', 'Stria medullaris thalami', 'Dorsal longitudinal fasciculus', '4-Hydroxy-3-Methoxyphenylacetic Acid', '3 Methoxy 4 Hydroxyphenylacetic Acid', 'Amfonelic acid', 'Nomifensina', 'Diclofensine', 'Nomifensine Maleate', 'Globus pallidus external segment', 'DOPAC - Dihydroxyphenylacetic acid', 'Dopamine formation', 'D3 dopamine receptor binding', 'Catecholamine formation', 'Remoxiprida', 'Butyrophenone derivatives', 'Amisulprida', 'Reduced haloperidol', 'Savoxepine', 'Veralipride', 'Cis-Flupenthixol', 'Olanzapine-fluoxetine combination', 'Zetidoline', '9 OH risperidone', 'Moperone', 'Haloperidol Dose', 'Olanzapine Dose', 'Cyclosomatostatin', 'Diphenylbutylpiperidine', 'Flufenazina', 'Fluphenazine Decanoate', 'Flupenthixol decanoate', 'Fluphenazine enanthate', 'Fluphenazine hydrochloride', 'Fluphenazine sulfoxide', 'Fluphenazine hcl', 'ZUCLOPENTHIXOL ACETATE', 'Zuclopenthixol decanoate', 'Zuclopenthixol dihydrochloride', 'Molindone Hydrochloride', 'Timiperone', 'Lenperone', 'Amfetamines', 'Amphetamine/Methamphetamine', 'Amphetamine misuse', 'Psychostimulant withdrawal', 'Levoamphetamine', 'Dextroamphetamine Sulfate', 'Orthostatic edema', 'Methcathinone', 'Methylone', 'Cathine', 'Methylenedioxypyrovalerone', 'Butylone', 'Naphyrone', 'Pyrovalerone', 'Methedrone', 'Flephedrone', 'Pentedrone', 'Pentylone', 'Buphedrone', 'Ethylone', 'Ethcathinone', 'Khat abuse', 'Substituted cathinone', 'PHENMETRAZINE HYDROCHLORIDE', 'Desoxypipradrol', 'Hydroxyamphetamine Hydrobromide', 'Hydroxynorephedrine', 'Vesicular Monoamine Transport Proteins', 'Vesicular Biogenic Amine Transport Proteins', 'Dihydrotetrabenazine', 'Monoamine Vesicular Transporter', 'Methoxytetrabenazine', '18F-FP-DTBZ', 'Vesicular monoamine transporter 1', 'Epithalamic structure', 'Monoaminergic cell groups', 'Vanillyl Mandelic Acid', 'Secologanin synthase', 'Strictosidine glucosidase', 'Strictosidine synthase activity', 'Oxidopamine', 'Nigrostriatal pathway', 'Substantia nigra pars reticulata', 'MPTP Poisoning', 'Striatonigral Degeneration', 'Neuromelanin', 'Pars compacta', 'Pars reticulata', 'Glial cytoplasmic inclusion', 'Dopaminergic Cell', 'Substantia Nigra Reticulata', 'Median forebrain bundle', 'Substantia Nigra Compacta', 'Caudal linear nucleus', 'Nucleus tegmenti pedunculopontinus', 'Nigrostriatal degeneration', 'Nigrostriatum', '1-Methyl-4-phenylpyridine', 'Dopamine melanin', '5-S-cysteinyldopamine', 'Interfascicular Nucleus', 'Somatodendritic dopamine release', 'Lewy neurite', 'WDR45', 'SKP1A', 'Globus pallidus internal segment', 'Central gray substance', 'Lenticular fasciculus', 'Brain iron deposition', 'Substantia Nigra Pars Lateralis', 'Marinesco body', 'Dopaminochrome', 'Paranigral nucleus', 'Nucleus paranigralis', 'PITX3 gene', 'Girisopam', 'Cerebral dopamine neurotrophic factor', 'Embryonic mesencephalon', 'Crus cerebri', 'Lateral globus pallidus', 'Medial medullary lamina', "2'-CH3-MPTP", 'Medial globus pallidus', 'Linear nucleus', 'Pars reticularis', 'Medial pallidal segment', 'Entire substantia nigra', 'Lateral pallidal segment', 'Area tegmentalis ventralis', 'Left substantia nigra', 'Right substantia nigra', 'Nucleus Linearis', 'Dopaminergic cell groups', 'Mesolimbic pathway', 'Mesocortical pathway', 'Laterodorsal tegmentum', 'Rostromedial tegmental nucleus', 'Serotonin 3 Receptors', 'Left substantia nigra pars compacta', 'Dopamine Plasma Membrane Transport Proteins', 'Norepinephrine Plasma Membrane Transport Proteins', 'DAT Dopamine Transporter', 'Vesicular monoamine transporter 2', 'Monoamine transporter', '123I-FP-CIT', 'GBR-12935', 'Dopamine transport', 'RTI-55', 'Cocaine binding', 'Benzatropina', 'WIN-35428', 'Cocaine receptors', '123I-Ioflupane', 'DA Transporter', 'RTI-121', 'Dimethocaine', 'Valbenazine', 'Ioflupane I-123', 'Altropane', 'Phenyltropane', 'Tc-99m-TRODAT-1', 'RTI-336', 'Technetium-99m TRODAT-1', 'Dopamine Transporter 1', 'Dopamine transporter deficiency syndrome', 'Bacterial Leucine Transporter', 'DAT activity', 'Stereotyped behaviour', 'Piribedil', 'N-n-propylnorapomorphine', 'N-propylnorapomorphine', 'R-(-)-apomorphine', 'Roxindole', 'Startle Gating', 'Apomorphine Hydrochloride', 'Nucleus amygdaloideus centralis', 'Apocodeine', 'Spiramide', 'Propylnorapomorphine', 'Apomorphine hcl', 'Emetic agents', 'Diacetylapomorphine', 'Norapomorphine', 'Erection frequency', 'Dopaminergic blocking agent', 'DAi receptors', 'Dopamine receptor site', 'Propyl-norapomorphine', 'Persephin', 'GDNF Family Ligands', 'GDNF Family Receptor Alpha-2', 'Neurturin Gene', 'Hydroxydopamines', '6-aminodopamine', 'GDNF Receptors', 'GDNF secretion', 'Delta wave', 'Unihemispheric slow-wave sleep', 'Activation-synthesis hypothesis', 'Flowerpot technique', 'Delta wave sleep', 'Volinanserin', 'Local sleep', 'Sleep inertia', 'Cognitive neuroscience of dreams', 'Multiple independent spike foci', 'Suppression-burst pattern', 'Jeavons syndrome', 'Erratic myoclonus', 'GNAO1 Gene', 'Parietal lobe epilepsy', 'Intractable occipital lobe epilepsy', 'Benign Occipital Epilepsy', 'Geschwind syndrome', 'Atypical absence epilepsy', 'Multifocal discharges', 'Retinal waves', 'Photoisomerase', 'Bistratified cell', 'Parasol cell', 'Midget cell', 'Ctenophorus ornatus', 'Oncomodulin', "Bruch's basal membrane", 'Retinoid isomerase', 'Retinol isomerase', 'Leber congenital amaurosis type 2', 'Retinol isomerase activity', 'Gene therapy for color blindness', 'Interstitial retinol-binding protein', 'Cone matrix sheath', 'Best Macular Dystrophy', 'Autosomal recessive bestrophinopathy', 'Autosomal dominant vitreoretinochoroidopathy', 'Bestrophins', 'BESTROPHIN 2', 'Bestrophin Family', 'Retinal Photoreceptor Cell Outer Segment', 'Retinal Photoreceptor Cell Inner Segment', 'Photoreceptor outer segment membrane', 'Leber amaurosis', 'CRB1', 'GUCY2D gene', 'Severe early childhood onset retinal dystrophy', 'Hereditary Optic Neuroretinopathy', 'AIPL1 gene', 'RPGRIP1 gene', 'PRPF31', 'IMPDH1 gene', 'RLBP1 gene', 'NR2E3 gene', 'Nyctalopin', 'Incomplete congenital stationary night blindness', 'Complete congenital stationary night blindness', 'CACNA1F gene', 'X-linked congenital stationary night blindness', 'Impaired night vision', 'ALAND ISLAND EYE DISEASE', 'Multifocal technique', 'N95 amplitude', 'Oligocone trichromacy', 'Cone dysfunction syndrome', 'Rod spherule', 'Scanning laser polarimeter', 'Radiatio optica', 'Juvenile x-linked retinoschisis', 'Peripheral schisis', 'Vitreous veils', 'Retinoschisin Protein', 'Mid-frequency hearing loss', 'Alpha-Tectorin', 'TECTA Gene', 'Traumatic optic nerve injury', 'OPN5', 'RODS CONES', 'Encephalopsin', 'ARNTL Transcription Factors', 'Cryptochrome-1', 'DNA Photolyases', 'CRYPTOCHROME 2', 'Cryptochrome Proteins', 'Period Circadian Proteins', 'CLOCK Proteins', 'PER2', 'PER1', 'Period (gene)', 'Circadian Clock Associated 1', 'NPAS2', 'ARNTL', 'PER3', 'REV-ERB-ALPHA', 'Doubletime', 'CSNK1D', 'TIMELESS gene', 'Period Proteins', 'ARNTL Gene', 'ARNTL2', 'RAR-related orphan receptor alpha', 'Familial advanced sleep phase syndrome', 'NPAS2 gene', 'BHLHE41', 'Principal clock', 'Oscillating gene', 'Retinohypothalamic tract', 'SCN Neurons', 'Irregular sleep–wake rhythm', 'Suprachiasmatic Nucleus Cells', 'Free-running sleep', 'Corpora arenacea', 'Pineal stalk', 'Pineal recess', 'Mouse Pineal Gland', 'AANAT activity', 'Pineal Parenchyma', 'Pineal structure', 'Rat Pineal Organ', 'Acetyl CoA Arylamine N Acetyltransferase', 'AANAT gene', 'Arylalkylamine N-Acetyltransferase', 'Acetylserotonin O-methyltransferase', 'Melatonin biosynthetic process', 'Acetylserotonin methyltransferase', 'Melatonin formation', 'Aralkylamine N-acetyltransferase', 'Arylalkylamine N-acetyltransferase activity', 'Nervus pinealis', 'N-Acetyl-2-Aminofluorene', 'Serotonin N-acetyltransferase activity', 'Serotonin Acetyltransferase', 'Arylamine N-acetyltransferase activity', 'Non-24-hour sleep–wake disorder', 'Melatonin receptor binding', 'Preperidinium', 'Diplopsalopsis', 'Complex partial seizure disorder', 'Temporal lobe sclerosis', 'Temporal lobe origin', 'Stereoelectroencephalography', 'Eeg electroencephalography', 'Anterior temporal lobectomy', 'Wada test', 'MEG - Magnetoencephalography', 'Corpus callosotomy', 'Amygdalohippocampectomy', 'TLE - Temporal lobe epilepsy', 'ECoG - Electrocorticography', 'Ictal-Interictal SPECT Analysis by SPM', 'Extratemporal epilepsy', 'Multiple subpial transection', 'Intracranial Electroencephalography', 'Functional hemispherectomy', 'Intracarotid amobarbital test', 'Intraoperative Electrocorticography', 'Electrocortical Stimulation Mapping', 'Extraoperative Electrocorticography', 'Mesial temporal lobe sclerosis', 'Hyperkinetic seizures', 'Engel classification', 'Intraoperative ECoG', 'Partial callosotomy', 'Hemispherectomies', 'Intracranial EEGs', 'Partial seizure disorder', 'Complete callosotomy', 'Abdominal aura', 'Intractable frontal lobe epilepsy', 'Extraoperative ECoG', 'Temporal lobe epilepsy syndrome', 'Refractory frontal lobe epilepsy', 'Amobarbital Injection', 'Major Epilepsy', 'Collateral Sulcus', 'Pes hippocampi', 'Right parahippocampal gyrus', 'Left parahippocampal gyrus', 'Lateral occipitotemporal gyrus', 'Granule cell dispersion', 'Congenital porencephaly', 'Simple partial seizures', 'Bathing epilepsy', 'Hyperorality', 'Inferior limiting sulcus', 'Left limbic lobe', '4-Aminobutyrate Transaminase', 'Mood stabilizing agent', 'Bipolar clinic', 'Vigabatrine', 'Vigabatrina', 'Gamma-Vinyl-GABA', 'Visual field constriction', 'GABA transaminase inhibitor', 'Symptomatic Infantile Spasms', 'Concentric visual field constriction', 'Refractory infantile spasms', 'Tiagabine Hydrochloride', 'Tiagabine hcl', 'GABA reuptake inhibitor', 'Nipecotic acid hydrochloride', '2-phenylpropenal', 'Etosuximida', 'Mesuximide', 'Methsuximide', 'Ethotoin', 'Phensuximide', 'N-desmethylmethsuximide', 'Pheneturide', 'Trimethadion', 'Ethosuximid', 'Phenylethylmalonamide', 'Methylphenobarbitone', 'PHENOBARBITAL/PHENYTOIN', 'Primidone+Phenobarbital', 'Childhood convulsions', 'Bilateral electroconvulsive therapy', 'Lower seizure threshold', 'Fosphenytoine', 'Fosphenytoin Sodium', 'Dimethadione', 'Phenacemide', 'Paramethadione', 'SL-75102', 'Nafimidone alcohol', 'Oxcarbazepina', 'Eslicarbazepine acetate', 'Licarbazepine', '10-hydroxycarbazepine', 'Oxcarbazepine Oral Suspension', 'Grand Mal Status Epilepticus', 'Diazepam Rectal Gel', 'Depakote er', 'Phenytoin sodium injection', 'Distal phalangeal hypoplasia', 'Cevimelina', 'Cevimeline hydrochloride', 'Valrocemide', 'Seletracetam', 'Unilateral Megalencephaly', 'MPPH syndrome', 'Plan for Achieving Self Support', 'Cysteine Loop Ligand-Gated Ion Channel Receptors', 'Xerocytosis', 'PIEZO1 gene', 'Golgi neuron', 'Dorsal paraflocculus', 'Bergmann glial cell', 'Olivocerebellar fibres', 'Nucleus interpositus anterior', 'Nucleus interpositus posterior', 'Lurcher Mice', 'GRID2 gene', 'Medullomyoblastomas', 'Anterior interposed nucleus', 'Nuclei pontis', 'REM rebound', 'Angular vestibuloocular reflex', 'Smooth pursuit abnormalities', 'Saccadic smooth pursuit', 'Abnormal pursuit', 'Macrosaccadic oscillations', 'Saccadic pulses', 'Medial eye fields', 'Hypermetric saccades', 'Chronostasis', 'Accommodative excess', 'Primary Motor Areas', 'Secondary Motor Areas', 'Brodmann area 4', 'Left primary motor cortex', 'Secondary Motor Cortices', 'Right abductor pollicis brevis', 'Right primary motor cortex', 'Left central sulcus', 'Right central sulcus', 'Beta-Adrenergic Agonist', 'Alpha 2 adrenergic agonist', 'Beta-2 Adrenergic Agonists', 'TRECADRINE', 'Mouse Iris', 'Bretylium Compounds', 'Bretylium Tosilate', 'Bethanidine Sulfate', 'Xylocholine', 'Alpha-Dihydroergocryptine', 'Apogalanthamine', 'Dichloroisoprenaline', 'GUANADREL SULFATE', 'Nucleus cuneatus', 'External cuneate nucleus', 'Cuneocerebellar tract', 'Lateral cuneate nucleus', 'Cuneate fasciculus', 'Granular insula', 'Primary somatic sensory cortex', 'Right abductor pollicis brevis muscle', 'Left abductor pollicis brevis', 'Abductor digiti minimi muscle of hand', 'Abductor digiti minimi muscle of foot', 'Split hand syndrome', 'Abductor digiti minimi muscle flap', "Musician's cramp", 'Hand muscle atrophy', 'Magnetic seizure therapy', 'Vagus nerve stimulator', 'Left vagus nerve', 'VOICE ALTERATION', 'Jugular ganglion', 'Ambiguus nucleus', 'Posterior tibial nerve block', 'Tarsal tunnel decompression', 'Batrachotoxins', 'Sodium Channel Activators', 'Phyllobates aurotaenia', 'Homobatrachotoxin', 'Colombian arrow poison', 'Batrachotoxinin A 20-alpha-benzoate', 'Genus Phyllobates', 'Lagocephalus inermis', 'Cephalothrix simula', 'Tetrodonic acid', 'Takifugu poecilonotus', 'Atelopus chiriquiensis', 'Zetekitoxin', '1-Methyl-3-isobutylxanthine', '3-Isobutyl-1-methylxanthine', '4-(3-Butoxy-4-methoxybenzyl)-2-imidazolidinone', 'Oxotremorine M', 'Milameline', 'Talsaclidine', 'Rectococcygeus', 'Nucleus praepositus', 'Phrenic nerve dysfunction', 'Chlamydomonas noctigama', 'Tarsal tunnel release', 'Tibial nerve compression', 'Medial parabrachial nucleus', 'Meobentine', 'Pudendal Nerve Entrapment Syndrome', 'Palmomental reflex', 'Tonic labyrinthine reflex', 'Clasp-knife response', 'Ciliospinal reflex', 'Simultaneous polydrug use', 'Heroin overdoses', 'Speedballs', 'MT-45', 'Acetylfentanyl', 'Alcohol cue', 'Pornography addiction', 'Tabernanthine', 'Three wall orbital decompression', 'Primary optic nerve sheath meningioma', 'Optociliary shunt vessels', 'Secondary ONSM', 'Primary ONSM', 'Bimatoprost', 'Dorzolamida', 'Brimonidina', 'Travoprost', 'Levobunolol', 'Brinzolamide', 'Unoprostone', 'Tafluprost', 'Apraclonidina', 'Prostamide', 'Unoprostone Isopropyl', 'Dorzolamide/Timolol', 'Episcleral veins', 'Latanoprostene Bunod', 'Latanoprost/timolol', 'Alphagan P', 'Ocular hyperemia', 'Levobunolol Hydrochloride', 'Apraclonidine Hydrochloride', 'Brinzolamide Ophthalmic Suspension', 'Brimonidine Purite', 'Dorzolamide-timolol combination', 'Bimatoprost + Timolol', 'Ocular hyperaemia', 'Preglaucoma', 'Timolol dorzolamide', 'Bimatoprost Ophthalmic Solution', 'Travoprost Ophthalmic Solution', 'Tafluprost Ophthalmic Solution', 'Bilateral primary open angle glaucoma', "Schlemm's canal", 'Myocilin', 'Scleral spur', 'Krukenberg spindles', 'Schwalbe line', 'MYOC protein', 'TIGR protein', 'Filtering surgery', 'Trabeculotomy', 'Filtration surgery', 'Deep sclerectomy', 'Filtering bleb', 'ANTIGLAUCOMA MEDICATIONS', 'Shallow anterior chamber', 'Choroidal effusion', 'Uveitic glaucoma', 'Developmental glaucoma', 'Trabectome', 'Minimally invasive glaucoma surgery', 'Trabeculotomy ab externo', 'Flat anterior chamber', 'Aqueous shunt', 'Glaucoma triple procedure', 'Bleb associated endophthalmitis', 'Glaucoma drainage surgery', 'Angle recession glaucoma', 'Laser goniopuncture', 'Leaking filtering bleb', 'Bleb related endophthalmitis', 'Serous choroidal detachment', 'Seidel test', 'Low intraocular pressure', 'Baerveldt tube shunt', 'Closure-angle glaucoma', 'TRABECULOTOME', 'Conjunctival wound', 'Glaucoma procedures', 'Trabeculoplasties', 'Trabeculectomy revision', 'Close angle glaucoma', 'Trabeculotomies', 'Advanced open-angle glaucoma', 'Ocular trabeculectomy', 'Baerveldt Implants', 'Glaucoma shunt device', 'Juvenile open angle', 'Goniotomies', 'Shallow AC', 'Betaxolol', 'Dorzolamide', 'Carteolol', 'Brimonidine Tartrate', 'Metipranolol', 'Dipivefrine', 'Befunolol', 'Antiglaucoma drug', 'DORZOLAMIDE HYDROCHLORIDE', 'Dipivefrin', 'Dipivefrina', 'Betaxolol Hydrochloride', 'Carteolol Hydrochloride', 'Dorzolamid', 'Dipivefrin Hydrochloride', 'Dipivalyl epinephrine', 'Levobetaxolol', 'Befunolol hydrochloride', 'Timolol eye drops', '8-hydroxycarteolol', 'Gel Forming Solution', 'BRIMONIDINE/TIMOLOL', 'Maleate timolol', 'Timolol Maleate Gel Forming Solution', 'Timoptic-XE', 'Lowered intraocular pressure', 'Dihydrolevobunolol', 'Pilocarpine / Timolol', 'Betaxolol Ophthalmic Solution', 'Betaxolol hcl', 'Timolol Dose', 'Timolol Ophthalmic Solution', 'Iris pigmentation', 'Isopropyl unoprostone', 'Orbital fat atrophy', 'Prostanoid FP receptor', 'Travatan Z', 'Latanoprost Ophthalmic Solution', 'Tafluprost acid', 'PG ANALOGUES', 'Plateau iris', 'Plateau iris syndrome', 'Laser peripheral iridoplasty', 'Plateau iris configuration', 'Laser iridectomy', 'Secondary angle-closure glaucoma', 'Chronic primary angle closure glaucoma', 'Laser gonioplasty', 'Bilateral angle-closure glaucoma', 'Peripheral iridoplasty', 'Bilateral acute angle-closure glaucoma', 'Surgical peripheral iridectomy', 'Low Tension Glaucoma', 'Glaucoma normal tension', 'Disc hemorrhage', 'Optineurin Gene', 'Black eye', 'Eye floaters', 'Angle recession', 'Uveitis-glaucoma-hyphema syndrome', 'UGH syndrome', 'Traumatic hyphema', 'Corneal blood staining', 'Scleral rupture', 'Traumatic hyphaema', 'Traumatic iritis', 'Spontaneous hyphema', 'Traumatic mydriasis', 'Spontaneous hyphaema', 'Total hyphema', 'Primary angle closure suspect', 'Peripheral anterior synechiae', 'Subacute angle-closure glaucoma', 'Indentation gonioscopy', 'Drainage angle', 'Iris processes', 'Indirect gonioscopy', 'Lens pseudoexfoliation', 'Exfoliation Glaucoma', 'Lysyl oxidase like 1', 'Glaucoma capsulare', 'Glaucoma hemifield test', 'Lenticular myopia', 'Progressive iris atrophy', 'Neuroretinal rim width', 'Large optic discs', 'Air-puff tonometer', 'Hemorrhagic choroidal detachment', 'Annular choroidal detachment', 'Laser sclerostomy', 'Sclerostomies', 'Aqueous misdirection', 'Ciliary block glaucoma', "Schwalbe's line", 'Perkins applanation tonometry', 'Ahmed tube', 'Laser iridoplasty', 'Pachymeters', 'Lens particle glaucoma', 'Horizontal corneal diameter', 'Vertical corneal diameter', 'Limbal hyperaemia', 'Ciliary flush', 'Glaucomatous visual field defect', 'Functional visual field loss', 'Peripheral visual field loss', 'Manual kinetic perimetry', 'Arcuate scotomas', 'Swedish interactive thresholding algorithm', 'Homonymous quadrantanopia', 'Confrontation visual field test', 'Small optic discs', 'Optic cup (embryology)', 'Iris nevus syndrome', 'Potassium acesulfame', 'CALCIUM CYCLAMATE', 'Advantame', 'GNAT3', 'Diffuse chemosensory system', 'Capparis masaikai', 'Mabinlin', 'Pentadin', 'Dioscoreophyllum', 'Richadella dulcifica', 'Pentadiplandraceae', 'Pentadiplandra', 'Posterior lingual gland', 'Facies inferior linguae', 'T1R receptor', 'Taste Transduction Pathway', 'Bitter taste perception', 'PROP TASTING', 'T2R receptors', 'TAS2R10', 'TAS1R2', 'TAS1R1', 'Lactisole', 'Barusiban', 'Tocolytic drug', 'Atosiban Acetate', 'L-368,899', 'Vaginal plethysmography', 'Chortophaga', 'Left intraparietal sulcus', 'Inferior frontal sulcus', 'Postcentral sulcus', 'Inferior precentral sulcus', 'Right intraparietal sulcus', 'Left superior parietal lobule', 'Right superior parietal lobule', 'Velamen', 'Cellufluor', 'TIK-301', 'Mebezonium Iodide', 'Mebezonium', 'Lignocaine+prilocaine', 'Felypressine', 'Felipresina', 'Spiral limbus', 'Hypoplastic cochlea', 'Phenomenal concept strategy', 'TrkC Receptor', 'Supratrochlear nerve', 'Supraorbital nerve block', 'Zygomaticotemporal nerve', 'Right supraorbital nerve', 'Stapedius tendon', 'Koniocellular cell', 'Patient DF', 'Vision for perception and vision for action', 'Dorsal lateral geniculate nucleus', 'Ventral lateral geniculate nucleus', 'LGN - Lateral geniculate nucleus', 'PGO waves', 'Pregeniculate nucleus', 'Ocular dominance column', 'Monocular deprivation', 'Footedness', 'Foot preference', 'Dunlop test', 'Accessory Abducens Nucleus', 'Nictitating membrane reflex', 'Nictitans Gland', 'Anterior interpositus nucleus', 'Cortical lobule', 'Internal Geniculate Body', 'Suprageniculate nucleus', 'Medial geniculate complex', 'Pteronotus quadridens', 'Mormoops blainvillei', 'Family Mormoopidae', 'Yuma myotis', 'Superior olivary nucleus', 'Superior Olives', 'Lateral superior olivary nucleus', 'Medial superior olivary nucleus', 'Cochlear nuclear complex', 'Superior Paraolivary Nucleus', 'Ventral acoustic stria', 'Intermediate acoustic stria', 'Periolivary Nucleus', 'Lateral lemniscal nuclei', 'Dorsomedial periolivary nucleus', 'Filtered speech test', 'Motor conduction block', 'Acquired polyneuropathy', 'Right inferior colliculus', '(R)-methanandamide', 'Mirfentanil', 'Knollenorgan', 'Passive electrolocation in fish', 'Gnathonemus petersi', 'Brienomyrus niger', 'Pollimyrus', 'Electric mormyrid', 'Stereocilium', 'Ciliated metaplasia', 'Cochlear amplifier', 'Prestin', 'Inner hair cells', 'Outer Auditory Hair Cells', 'Cuticular plate', 'Deiters cells', 'Cochlear Outer Hair Cells', 'Inner spiral sulcus', 'Cochlear Inner Hair Cells', 'Entire cochlea', 'Spiral Organs', 'Transcription Factor Brn-3C', 'ATOH1 Gene', 'Stereocilia', 'Collapsin response mediator protein-2', 'CRMP1', 'Lanthionine Ketimine', 'Pioneer neuron', 'Netrin receptor', 'DCC Receptor', 'UNC5C', 'Netrin-1 Receptors', 'UNC5C gene', 'Netrin Family', 'Netrin Receptor DCC', 'SEMA4D', 'Sema domain', 'Semaphorin-6A', 'SEMA4D Gene', 'Rho GTPase binding', 'SLIT3', 'SLIT1', 'Slit2 protein', 'SLIT3 Gene', 'Robo protein', 'ROBO1 Gene', 'Repulsive guidance molecule A', 'SEMA3F Gene', 'Dendritic knob', 'Olfactory Receptor Proteins', 'Olfactory Transduction Pathway', 'Olfactory Sensory Cilia', 'Olfactory Epithelial Cell', 'Olfactory glands', "Bowman's glands", 'Olfactory sensory epithelium', 'Vomeronasal Nerves', 'Finger agnosia', 'Right-left disorientation', 'Cortical aphasia', 'Oscillatoria perornata', 'Dapiprazol', 'Anterior semicircular canal', 'Semont maneuver', 'Benign paroxysmal positional nystagmus', 'Posterior ampullary nerve', 'Osseous ampullae', 'Tullio phenomenon', 'Superior semicircular canal dehiscence syndrome', 'Autophony', 'Arcuate eminence', 'Michel deformity', 'Enlarged vestibule', 'Right lateral semicircular canal', 'Superior vestibular nucleus', 'Prepositus hypoglossal nucleus', 'Inferior vestibular nucleus', 'Spinal Vestibular Nucleus', 'Deiters Nucleus', 'Dix-Hallpike maneuver', 'Migraine equivalents', 'Central positional nystagmus', 'Central positional vertigo', 'Nystagmus direction', 'Blepharospasm-Oromandibular Dystonia', 'Eyelid spasms', 'ICCA SYNDROME', 'Infantile convulsions and choreoathetosis', 'Abductor spasmodic dysphonia', 'Noradrenergic cells', 'Dorsal acoustic stria', 'Posteroventral cochlear nucleus', 'Cochleotomy', 'Auditory Brain Stem Implants', 'Auditory Brain Stem Implantation', 'Mandibular hyperplasia', 'Relative mandibular prognathism', 'Short metatarsal', 'Short fourth metatarsal', 'Vesicular Acetylcholine Transport Proteins', 'Vesamicol', 'Acetylcholine transporter', 'Benzovesamicol', 'High-affinity choline transporter', 'Rubreserine', 'Iliocostalis lumborum muscle', 'Spinalis Thoracis', 'Genetic epistemology', 'Formal epistemology', 'Meta-epistemology', 'Causal theory of knowledge', 'Epistemology of Wikipedia', 'Observationalism', 'Social identity model of deindividuation effects', 'Neoevolutionism', 'Social tuning', 'Group dynamics', 'Group polarization', 'Social entropy', 'Conscientiousness', 'Eysenck Personality Questionnaire', 'Psychoticism', 'Agreeableness', 'Extraversion (Psychology)', 'Introversion (Psychology)', 'Neuroticism Traits', 'Trait theory', 'Hierarchical structure of the Big Five', 'Personality dimension', 'Big Five Inventory', 'Revised NEO Personality Inventory', 'International Personality Item Pool', 'Communibiology', 'Lexical hypothesis', 'Quarrelsomeness', 'Introvert personality', 'Introverted personality', 'Religion and personality', 'Multiple personality traits', 'Facet (psychology)', 'Biological basis of personality', 'Critical positivity ratio', 'Unstable personality', 'Transmarginal inhibition', 'Measure personality', 'Emotionally stable', 'Patient personality traits', 'ESFJ', 'Emotionally unstable personality', 'ESTJ', 'ENFP', 'HEXACO model of personality structure', 'Personality in animals', 'ISFJ', 'INFJ', 'ISTJ', 'Two-factor models of personality', 'Tridimensional Personality Questionnaire', 'Self-transcendence', 'Self-report inventory', 'Cattell Personality Factor Questionnaire', '16PF Questionnaire', 'Myers-Briggs Type Indicator', 'Alternative five model of personality', 'Absorption (psychology)', 'Happy personality', 'Self-directedness', 'Splitting', 'Malignant narcissism', 'Positive emotionality', 'Easy temperament', 'Schizoid personality disorder', 'Borderline schizophrenia', 'Narcissistic supply', 'Schedule for Nonadaptive and Adaptive Personality', 'Histrionic personality disorder', 'Dependent personality disorder', 'Paranoid personality disorder', 'Sexual Sadism', 'Passive-Aggressive Personality Disorder', 'Depressive personality disorder', 'Specific personality disorders', 'Chinese Classification of Mental Disorders', 'Self-defeating personality disorder', 'Management of borderline personality disorder', 'Hysterical personality disorder', 'Personality disorder cluster', 'Psychopathic Personality Inventory', 'Psychopathic personality disorder', 'Psychopathic personality trait', 'Difficulty communicating feelings', 'Job enrichment', 'Core self-evaluations', 'Gainful employment', 'Job demands-resources model', 'Job rotation', 'Contextual performance', 'Personnel psychology', 'Job shadow', 'Job characteristic theory', 'Job enlargement', 'Characteristics job', 'Affective events theory', 'Human relations movement', 'Leaving job', 'M. procerus', 'Behavioral systems analysis', 'Organizational safety', 'Organizational space', 'Theory X and Theory Y', 'Organizational information theory', 'Imprinting (organizational theory)', 'Dispute Systems Design', 'Uniform Domain-Name Dispute-Resolution Policy', 'Lawyer supported mediation', 'Family dispute resolution', 'Mediation in Australia', 'Transformative mediation', 'Dispute board', 'Legal dispute resolution', 'Snowflake schema', 'Superkey', 'Fact constellation', 'Schema (genetic algorithms)', 'Derealization', 'Depersonalization Disorder', 'Depersonalisation disorder', 'Depersonalization-derealization disorder', 'Depersonalization syndrome', 'Cross-cultural leadership', 'Path–goal theory', 'Situational theory of publics', 'Vroom–Yetton decision model', 'Helleborus thibetanus', 'Helleborus lividus', 'Helleborus multifidus', 'Helleborus odorus', 'Genus Helleborus', 'Osteospermum ecklonis', 'Osteospermum fruticosum', 'Calibrachoa parviflora', 'Astilbe x arendsii', 'Forsteronia', 'Mesechiteae', 'Prestonia', 'Mandevilla illustris', 'Mandevilla sanderi', 'Condylocarpon', 'Cascabela', 'Laubertia', 'Mesechites', 'Secondatia', 'Odontadenia', 'Hancornia', 'Rhodocalyx', 'Condylocarpon isthmicum', 'Basistemon', 'Angelonia angustifolia', 'Effort justification', 'Problematic integration theory', 'Financial abuse', 'Emotional neglect', 'Physical neglect', 'Economic abuse', 'Child emotional abuse', 'Adult sexual abuse', 'Emotional child abuse', 'Child abuse victim', 'Sexual abuse child', 'Adult physical abuse', 'Abuse elder', 'Mental health first aid', 'Involuntary outpatient commitment', 'Undifferentiated somatoform disorder', 'Approved social worker', 'Approved mental health professional', 'Disorders mood', 'Ziprasidona', 'Amperozide', 'Perospirone', 'Typical antipsychotic', 'Iloperidona', 'Desmethylclozapine', 'Thienobenzodiazepine', 'Dehydroaripiprazole', 'Tiospirone', 'Norquetiapine', 'Olanzapine/fluoxetine', 'Subchronic schizophrenia', 'RisperiDONE Injection', 'Clozapine overdose', 'Scale for the Assessment of Negative Symptoms', 'Thought disturbance', 'Premorbid Adjustment Scale', 'Barnes Akathisia Scale', 'Psychotic symptom rating scale', 'PANSS - Hostility', 'PANSS - Depression', 'Morningside rehabilitation status scale', 'PANSS - Excitement', 'Schizoaffective psychosis', 'Schizophreniform disorder', 'Brief psychotic disorder', 'Psychosis NOS', 'Psychotic disorder NOS', 'Incipient Schizophrenia', 'Prodromal States', 'Postdrome', 'Prodromal Syndromes', 'Schizophrenic prodrome', 'Schizotaxia', 'Cognitive slippage', 'Illogical thinking', 'Disordered Thinking', 'Thought disorder scale', 'Negative formal thought disorder', 'Positive formal thought disorder', 'Tardive psychosis', 'Undifferentiated schizophrenia', 'Disorganized schizophrenia', 'Chronic paranoid schizophrenia', 'DTNBP1 gene', 'Biogenesis of lysosome-related organelles complex 1', 'DYSTROBREVIN-BINDING PROTEIN 1', 'Shared Psychotic Disorder', 'Persistent delusional disorder', 'Somatic delusion', 'Soft sign', 'Abuse cannabis', 'Late paraphrenia', 'Acute polymorphic psychotic disorder', 'Bouffees delirantes', 'Thought broadcasting', 'Thought withdrawal', 'Psychogenic psychosis', 'Ziprasidone Hydrochloride', 'Ziprasidone hcl', 'Ziprasidone Mesylate', 'Ziprasidone Injection', 'Amisulpride 50 MG', 'LOXAPINE SUCCINATE', 'Sertindole', 'Quetiapine Fumarate', 'Zotepine', 'Dibenzothiazepine', 'Quetiapine hemifumarate', 'Ziprazidone', 'Seroquel XR', 'Norzotepine', 'Quetiapine 50 MG', 'Dehydrosertindole', 'Quetiapine metabolite', 'Tardive akathisia', 'PSEUDOPARKINSONISM', 'Pseudoakathisia', 'Drug induced akathisia', 'Inner Restlessness', 'Olanzapine pamoate', 'Invega Sustenna', 'Oral antipsychotic therapy', 'Asenapine maleate', 'Psychopharmacologic agent', 'Oral hypoesthesia', 'Lurasidone Hydrochloride', 'Lurasidona', 'Pre-pulse inhibition', 'Automatic obedience', 'Separation anxiety disorder', 'Penn State worry questionnaire', 'Specific phobia', 'Overanxious disorder', 'Simple phobia', 'Animal Phobia', 'GAD - Generalized anxiety disorder', 'Emetophobia', 'Anxiety disorder symptoms', 'Coping Cat', 'Generalized Anxiety Disorder 7', 'Generalized anxiety disorder 7 item scale', 'Generalized Anxiety Disorder Questionnaire', 'Worry Frequency', 'Panic Disorder with Agoraphobia', 'Interoceptive exposure', 'Panic disorder agoraphobia', 'Panic Disorder Severity Scale', 'Phobic avoidance', 'Cognitions questionnaire', 'Panic and Agoraphobia Scale', 'Childhood separation anxiety', 'Agoraphobia without history of panic disorder', 'Beck Anxiety Inventory score', 'NCCN Distress Thermometer', 'Tandospirone Citrate', 'FG-7142', 'Histaminergic Agents', 'Galphimine B', 'Galphimia', 'Probenecida', 'Treatment IND', 'Ethylmorphine-N-Demethylase', 'Norethylmorphine', 'Opiate Substitution Treatment', 'Patient attitude toward treatment', 'Heroin-assisted treatment', 'Levacetylmethadol', 'Methadone dose', 'Methadone treatments', 'Methadone clinic', 'Serum methadone level', 'Urine morphine test', 'Use Heroin', 'Urine morphine', 'Maintenance methadone', 'Plasma methadone level', 'LOFEXIDINE HYDROCHLORIDE', 'Acetilmetadol', 'Noracetylmethadol', 'Demand reduction policy', 'Pharmacogenomic Test', '1-benzylpiperazine', 'Potentially Inappropriate Medication List', 'Deprescriptions', 'STOPP START Criteria', 'Deprescription', 'Medicare part', 'Chondroplasties', 'Mycoplasma testudineum', 'Acute lower respiratory tract infection', 'Postoperative lower respiratory tract infection', 'Paramyxoviridae Infections', 'Coronavirus NL63', 'Human metapneumovirus infection', 'Metapneumoviruses', 'Pneumoviridae', 'Human respiratory virus', 'Subfamily Pneumovirinae', 'Respiratory syncytial virus B', 'Human metapneumovirus pneumonia', 'Genus Metapneumovirus', 'Genus Pneumovirus', 'Human metapneumovirus RNA', 'Human rhinovirus A', 'Parvoviridae Infections', 'Canine minute virus', 'Canine parvovirus type 1', 'Bocaparvovirus', 'Human bocaviruses', 'Genus Bocavirus', 'Human bocavirus DNA', 'Human coronavirus HKU1', 'Thoracic gas volume', 'Nitrogen washout', 'Helium dilution technique', 'FRC - Functional residual capacity', 'Closing capacity', 'Functional residual capacity measurement', 'Static lung volume', 'Single breath nitrogen washout test', 'Increased functional residual capacity', 'Esophageal balloon catheter', 'Proportional Assist Ventilation', 'Interactive Ventilatory Support', 'Continuous mandatory ventilation', 'Respiratory Dead Space', 'Anatomical dead space', 'Physiological dead space', 'Alveolar dead space', 'Bohr equation', 'Anatomic dead space', 'Pulmonary dead space', 'Dead space/tidal volume ratio', 'Physiological dead space/tidal volume ratio', 'Instrumental dead space', 'Mechanical dead space', 'Peak Expiratory Pressure', 'Peak inspiratory flow', 'Peak Inspiratory Flow Rate', 'Inspiratory gas flow', 'Biphasic Intermittent Positive Airway Pressure', 'Racemic Adrenaline', 'Klassevirus', 'Levator costae', 'Aproctoidea', 'Doxapram hcl', 'Dentinoid Formation', 'Benign Odontogenic Neoplasm', 'Ameloblastic Fibrosarcoma', 'Ameloblastic fibrodentinoma', 'Ameloblastic Fibroodontoma', 'Malignant odontogenic tumor', 'Extraosseous Ameloblastoma', 'Intraosseous Ameloblastoma', 'Granular cell odontogenic tumor', 'Odontogenic Ectomesenchyme', 'Metastasizing Ameloblastoma', 'Benign Ameloblastoma', 'Conventional Ameloblastoma', 'Squamous odontogenic tumour', 'Papilliferous keratoameloblastoma', 'Intracranial Plasma Cell Granuloma', 'Pulmonary Plasma Cell Granuloma', 'Follicular dendritic cell tumour', 'Pulmonary Inflammatory Pseudotumors', 'Orbital Inflammatory Pseudotumors', 'Sialo-odontogenic cyst', 'Botryoid odontogenic cyst', 'Mandibular infected buccal cyst', 'Buccal bifurcation cyst', 'Lateral radicular cyst', 'Inflammatory odontogenic cyst', 'Nerve Sheath Myxomas', 'Simplified acute physiology scale II', 'Mortality probability model II', 'SAPS III', 'ICU scoring systems', 'Childhood disintegrative disorder', 'Pervasive developmental disorder not otherwise specified', 'Multiple complex developmental disorder', "Heller's syndrome", 'Synthetic human secretin', 'Hemimaxillofacial dysplasia', 'Acute Stress Disorder', 'Autism Diagnostic Observation Schedule', 'Autism-spectrum quotient', 'Autistic traits', 'Social Responsiveness Scale', 'Autistic symptoms', 'Modified Checklist for Autism in Toddlers', 'Gluten-free, casein-free diet', 'BTBR Mouse', 'Aspergers disorder', 'Neurotypical', 'Pathological demand avoidance', 'ARBACLOFEN', 'Angiogenic Squamous Dysplasia', 'Autism Treatment Evaluation Checklist', 'Dup15q', 'Animal models of autism', 'Congenital atrial septal defect', 'Autism clinic', 'Childhood Autism Spectrum Test', 'Suspected autism', 'Precoproporphyrin', 'Aortic Rim', 'Epigenetics of autism', 'Hypomanic personality', 'Bipolar spectrum diagnostic scale', 'Bipolar disorder not otherwise specified', 'Racing thoughts', 'N-desmethyltramadol', 'Codeine acetaminophen', 'Ketorolac trometamol', 'Ophthalmic Dosage Form', 'Ketorolac Ophthalmic Solution', 'Pethidinic acid', 'BUCINNAZINE HYDROCHLORIDE', 'Metazocine', 'Cyclorphan', 'Levorfanol', 'Hydromorphone-3-glucuronide', 'Bisnortilidine', 'Anatalline', 'Dissolvable tobacco', 'Dissociative Amnesia', 'Dissociative Fugue', 'Dissociative disorder not otherwise specified', 'Methoxphenidine', 'Brief Pain Inventory (BPI)', 'Pain interference score', 'Atomoxetine hydrochloride', 'Tomoxetina', 'Selective norepinephrine reuptake inhibitor', 'ATOMOXETINE HCL', 'Magnesium pemoline', 'D-methylphenidate', 'Dexmethylphenidate Hydrochloride', 'RTS - Revised trauma score', 'Manual Ability Classification System', 'Triplegia', 'Fine Motor Delay', 'Medialization Laryngoplasties', 'Ixodes cornuatus', 'Holocyclotoxin', 'Sternomental distance', 'Mallampati class III', 'Macintosh laryngoscope blade', 'Miller laryngoscope blade', 'Laryngoscope handle', 'Artificial airway device', 'Intubating LMA', 'Tracheal hook', 'Eschmann tracheal tube introducer', 'Gamma-Cyclodextrins', 'Postoperative residual curarization', 'Sugammadex Sodium', 'Sugammadex Injection', 'Female Athlete Triad Syndrome', 'Detomidine hydrochloride', 'Atipamezol', 'Fluparoxan', 'Thiafentanil', 'Medetomidine hydrochloride', 'Atipamezole hydrochloride', 'N-ethylacetamide', 'Eszopiclone 3 MG', 'Impaired spontaneous ventilation', 'Adventitious breath sounds', 'Cervical myelocystocele', 'Persistent complex bereavement disorder', 'Protriptilina', 'Norzimelidine', 'Protriptyline Hydrochloride', 'Trimipramine Maleate', '2-hydroxyimipramine', 'Didesmethylcitalopram', 'Didemethylcitalopram', 'Sertraline hcl', 'Venlafaxine hcl', 'Desvenlafaxine Succinate', 'Desvenlafaxine 50 MG', 'Desmethylmianserin', 'Desmethylmirtazapine', 'Adult Extracardiac Rhabdomyoma', 'Right lymphatic duct', 'Thoracic lymphatic duct', 'Right thoracic duct', 'Psilocybe semilanceata', 'Copelandia', 'Baeocystin', 'Cotard delusion', 'Syndrome of subjective doubles', 'Logical behaviorism', 'Environmental social science', 'Protoscience', 'Mesology', 'Biology and political science', 'SAT Subject Test in Chemistry', 'SAT Subject Test in Physics', 'Definitions of mathematics', 'Structuralism (philosophy of mathematics)', 'Pre-algebra', 'Mathematically Correct', 'Integrated mathematics', 'Relationship between mathematics and physics', 'Comprehensive School Mathematics Program', 'The Harmful Effects of Algorithms in Grades 1–4', 'Interactive Mathematics Program', 'Chunking (division)', 'Part III of the Mathematical Tripos', 'Multiplication and repeated addition', 'Mathematics education in the United States', 'Investigations in Numbers, Data, and Space', 'DCDC2 gene', 'Proactive learning', 'Biomedical cybernetics', 'Alternative education', 'Eidetic memory', 'Certificate in Education', 'Operations and technology management', 'Business & Finance', 'Critical social thought', 'Complexity economics', 'International Society for Ecological Economics', 'AP Physics 1', 'Personalized learning', 'Team learning', 'Open educational practices', 'Interaction Design Foundation', 'Asynchronous learning', 'Synchronous conferencing', 'Axial coding', 'Curriculum-based measurement', 'Understanding by Design', 'Emergent curriculum', 'Heutagogy', 'Social learning in animals', 'Adventure therapy', 'Ropes course', 'Guyanese Creole', 'Auto-antonym', "Porter's generic strategies", 'Systematic musicology', 'Sociomusicology', 'Cantometrics', 'Embodied music cognition', 'Musical syntax', 'Biomusicology', 'Melodic expectation', 'Music semiology', 'Program music', 'Aesthetics of music', 'Through-composed', 'Formalism (music)', 'Middle Eastern music', 'Emotional geography', 'Xenharmonic music', 'Collaborative piano', 'Greeklish', 'Studies in Natural Language Processing', 'Picture language', 'Temporal annotation', 'Graphetics', 'Microlinguistics', 'Language and Communication Technologies', 'Grammar–translation method', 'Audio-lingual method', 'Community language learning', 'Synthetic language', 'Structured English', 'Linguistic demography', 'General English Proficiency Test', 'AP Spanish', 'AP German Language', 'AP Comparative Government and Politics', 'New Ways of Analyzing Variation', 'Language identification', 'Object language', 'Context-sensitive language', 'Chomsky hierarchy', 'Natural language programming', 'MultiNet', 'TimeML', 'Kosraean language', 'Cache language model', 'Metasyntax', "Hockett's design features", 'Gellish', 'Factored language model', 'Minimum information required in the annotation of models', 'Language identification in the limit', 'Folk linguistics', 'Integrational linguistics', 'Cognitive sociolinguistics', 'Economics of language', 'Language module', 'Language attrition', 'Pre-established harmony', 'Normative statement', 'Chemistry (relationship)', 'Pure submodule', 'Jacobson ring', 'Artinian module', 'Torsion-free module', "Citizen's arrest", 'Sketch-based modeling']
        # f = open('name.txt', 'r', encoding='utf-8')
        # data = f.read()
        # data_list = data.split('\n')
        # self.KeyWord = []
        # for i in data_list:
        #     self.KeyWord.append(i.strip(' '))
        print('KeyWork= ', self.KeyWord)
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=utf-8',
            # 'Referer': 'https://academic.microsoft.com/search?q=Medicine&f=&orderBy=0&skip=0&take=10',
            'X-Requested-With': 'Fetch',
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        }
        self.url = 'https://academic.microsoft.com/api/search'
        self.data = {
            "query": '',
            "queryExpression": "",
            "filters": [],
            "orderBy": 0,
            "skip": 0,
            "sortAscending": 'true',
            "take": 10,
            "includeCitationContexts": 'false'
        }
    def start_requests(self):
        for key in self.KeyWord:
            print('抓取第  {}  个关键词为   {}'.format(self.KeyWord.index(key), key))
            referer = 'https://academic.microsoft.com/search?q=Medicine&f=&orderBy=0&skip=0&take=10'
            self.headers['Referer'] = referer
            data = self.data
            data['query'] = key
            print('url= ', self.url)
            yield scrapy.Request(url=self.url, method='POST', headers=self.headers, body=json.dumps(data), meta={'key': key}, callback=self.FirstParse, dont_filter=True)

    def FirstParse(self, response):
        # print('++++++++++++parse++++++++++++++++')
        body = response.body
        key = response.meta['key']
        json_data = json.loads(body)
        data_list = json_data['pr']
        # 翻页数量
        Nums = json_data['t']
        print('Nums= ', Nums)
        pages = Nums // 10
        pages_ys = Nums % 10
        if pages_ys > 0:
            pages += 1
        for num in range(pages):
        # for num in range(3):
            #print('num的值= ', num)
            if num == 0:
                #print('data_list= ', data_list)
                for dt in data_list:
                    paper = dt['paper']
                    # 名称
                    name = paper['dn']
                    # 时间
                    date = paper['v']['publishedDate']
                    # 作者
                    # authors = [author['dn'] for author in paper['a']]
                    author_information = {}
                    author_index = 1
                    for information in paper['a']:
                        author_name = information['dn']
                        author_sources = information['i']
                        temp_list = []
                        temp_dict = {}
                        for author in author_sources:
                            author_source = ''
                            try:
                                author_source = author['dn']
                            except Exception as e:
                                pass
                            temp_list.append(author_source)
                        temp_dict[str(author_index)] = {
                            'author_name': author_name,
                            'author_source': temp_list
                        }
                        author_index += 1
                        author_information.update(temp_dict)

                    # 标签
                    tags = [tag['dn'] for tag in paper['fos']]
                    # 引文数量
                    citations = paper['eccnt']
                    # 关联关系页数
                    related_pages = paper['et']
                    # name_id
                    name_id = paper['id']
                    # 数据集介绍
                    datasetInformation = ''
                    try:
                        datasetInformation = paper['d']
                    except:
                        pass

                    page_dict = {
                        'name': name,
                        'datasetInformation': datasetInformation,
                        'date': date,
                        'authors': author_information,
                        'tags': tags,
                        'citations': citations,
                        'related_pages': related_pages,
                        'id': name_id
                    }
            # else:
            #     pass
            #         print('page_dict= ', page_dict)
                    reference_url = 'https://academic.microsoft.com/api/entity/{}?entityType=2'.format(page_dict['id'])
                    reference_headers = self.headers.copy()
                    reference_headers.pop('Content-Type')
                    reference_headers['Referer'] = 'https://academic.microsoft.com/paper/{}/reference'.format(page_dict['id'])
                    meta = {
                        'page_dict': page_dict
                    }
                    yield scrapy.Request(reference_url, method='GET', headers=reference_headers, meta=meta, callback=self.ReferenceParse, dont_filter=True)
            else:
                referer = 'https://academic.microsoft.com/search?q=Medicine&f=&orderBy=0&skip={}&take=10'.format(num*10)
                self.headers['Referer'] = referer
                data = self.data.copy()
                data['query'] = key
                yield scrapy.Request(url=self.url, method='POST', headers=self.headers, body=json.dumps(data), callback=self.TwoParse, dont_filter=True)

    def TwoParse(self, response):
        body = response.body
        json_data = json.loads(body)
        data_list = json_data['pr']
        for dt in data_list:
            paper = dt['paper']
            # 名称
            name = paper['dn']
            # 时间
            date = paper['v']['publishedDate']
            # 作者
            # authors = [author['dn'] for author in paper['a']]
            author_information = {}
            author_index = 1
            for information in paper['a']:
                author_name = information['dn']
                author_sources = information['i']
                temp_list = []
                temp_dict = {}
                for author in author_sources:
                    author_source = ''
                    try:
                        author_source = author['dn']
                    except Exception as e:
                        pass
                    temp_list.append(author_source)
                temp_dict[str(author_index)] = {
                    'author_name': author_name,
                    'author_source': temp_list
                }
                author_index += 1
                author_information.update(temp_dict)

            # 标签
            tags = [tag['dn'] for tag in paper['fos']]
            # 引文数量
            citations = paper['eccnt']
            # 关联关系页数
            related_pages = paper['et']
            # name_id
            name_id = paper['id']
            # 数据集介绍
            datasetInformation = ''
            try:
                datasetInformation = paper['d']
            except:
                pass
            page_dict = {
                'name': name,
                'datasetInformation': datasetInformation,
                'date': date,
                'authors': author_information,
                'tags': tags,
                'citations': citations,
                'related_pages': related_pages,
                'id': name_id
            }
            reference_url = 'https://academic.microsoft.com/api/entity/{}?entityType=2'.format(page_dict['id'])
            reference_headers = self.headers.copy()
            reference_headers.pop('Content-Type')
            reference_headers['Referer'] = 'https://academic.microsoft.com/paper/{}/reference'.format(page_dict['id'])
            meta = {
                'page_dict': page_dict
            }
            yield scrapy.Request(reference_url, method='GET', headers=reference_headers, meta=meta,
                                 callback=self.ReferenceParse, dont_filter=True)

    def ReferenceParse(self, responses):
        """
        有的论文有下载的文件，需要将他们保存下来,
        其中包含了两个需要的值：
                文件：
                下一次请求的queryExpression的值
        :param responses:
        :return:
        """
        # print('===========ReferenceParse============')
        reference_data = responses.body
        page_dict = responses.meta['page_dict']
        reference_jsondata = json.loads(reference_data)

        reference_dict = getReference(reference_jsondata)
        page_dict['reference_dict'] = reference_dict

        # 关联的 PaperExpression 的值
        relatedPaperExpression = reference_jsondata['relatedPaperExpression']

        data = self.data
        temp_dict = {
            'includeCitationContexts': 'true',
            'parentEntityId': page_dict['id'],
            'query': page_dict['name'],
            # 'queryExpression': queryExpression,
        }
        data.update(temp_dict)
        headers = self.headers
        headers['Referer'] = 'https://academic.microsoft.com/paper/{}/citedby/search?q={}&qe=RId%3D{}&f=&orderBy=0'.format(
            page_dict['id'], page_dict['name'], page_dict['id'])

        # 有reference的话那么queryExpression的值是paperReferencesExpression
        # 没有的话那么queryExpression的值是entityExpression
        try:
            queryExpression = reference_jsondata['paperReferencesExpression']
            is_references = 1
        except:
            # queryExpression = reference_jsondata['entityExpression']
            queryExpression = 'RId=' + str(page_dict['id'])
            is_references = 0
            # print('except queryExpression=', queryExpression)
        temp_dict['queryExpression'] = queryExpression
        data.update(temp_dict)
        meta = {
            'page_dict': page_dict,
            'is_references': is_references,
            'data': data.copy(),  # 这个地方一定要加copy,不然的话会被后面的值给跟新掉
            'relatedPaperExpression': relatedPaperExpression
        }
        yield scrapy.Request(self.url, method='POST', headers=headers, body=json.dumps(data), meta=meta, callback=self.ParseIsHaveReferences, dont_filter=True)

    def ParseIsHaveReferences(self, responses):
        """
        解析包含references的论文
        :param response:
        :return:
        """
        # print('**********PageParse************')
        page_dict = responses.meta['page_dict']
        is_references = responses.meta['is_references']
        data = responses.meta['data']
        relatedPaperExpression = responses.meta['relatedPaperExpression']

        page_data = responses.body
        json_data = json.loads(page_data)

        request_data = data.copy()
        # print('PAGE_DICT= ', page_dict)
        microsoft_datajson = page_dict.copy()
        # 判断是否有references
        references_jsondata = {}
        references_num = 0
        if is_references:
            # print('包含references===========')
            references_num = json_data['t']
            page_dict['references_num'] = references_num
            # print('references_num= ', references_num)
            # for i in range(references_num):
            references_jsondata = getReferencesData(references_num, page_dict, self.headers, self.url, request_data)

            # 将references的data的queryExpression更换掉，方便后面获取cited和related
            request_data['queryExpression'] = 'RId=' + str(page_dict['id'])
            # 因为有了reference，那么cited_num的值需要重新请求
            new_headers = self.headers.copy()
            new_headers['Referer'] = 'https://academic.microsoft.com/paper/{}/citedby/search?q={}&qe=RId%253D{}&f=&orderBy=0'.format(page_dict['id'], page_dict['name'], page_dict['id'])
            new_data = request_data.copy()
            new_data['skip'] = 0
            new_response = requests.post(self.url, headers=new_headers, data=json.dumps(new_data))
            # 默认值为：1
            cited_num = 1
            if new_response.status_code == 200:
                try:
                    text = new_response.text
                    json_data = json.loads(text)
                    cited_num = int(json_data['t'])
                except:
                    pass
            else:
                print('错误响应码为：', new_response.status_code)
        else:
            cited_num = int(json_data['t'])
        cited_jsondata = getCitedByData(cited_num, page_dict, self.headers, self.url, request_data)
        # 循环得到related, 这个值是页数
        related_pages = int(page_dict['related_pages'])
        # related_data = data.copy()
        related_jsondata = getRelatedData(related_pages, request_data, page_dict, self.headers, self.url, relatedPaperExpression)
        temp_dict = {
            'references_num': references_num,
            'cited_num': cited_num,
            'references_jsondata': references_jsondata,
            'cited_jsondata': cited_jsondata,
            'related_jsondata': related_jsondata,
        }
        microsoft_datajson.update(temp_dict.copy())
        # print('microsoft_datajson= ', microsoft_datajson)
        items = MicrosoftacademicItem()
        for k, v in microsoft_datajson.items():
            items[k] = v
        yield items



def parseNextPage(url, headers, cited_data, index):
    """
    解析下一页得到数据，其中包括references、cited by、 related的翻页
    :return:
    """
    # print('=========citedPage=========')
    response = requests.post(url, headers=headers, data=json.dumps(cited_data))
    data = ''
    if response.status_code == 200:
        text = response.text
        data_json = json.loads(text)
        data = parsePaperContent(index, data_json)
        # print('data= ', data)
    else:
        pass
        # print('cited 错误响应码为： ', response.status_code)
    return data

def getReference(reference_jsondata):
    """
    解析得到ViewPDF、Website、AdditionalLink
    :param reference_jsondata:
    :return:
    """
    reference_dict = {
        'ViewPDF': [],
        'Website': [],
        'AdditionalLink': []
    }
    try:
        reference_list = reference_jsondata['entity']['s']
        for i in reference_list:
            index = i['sourceType']
            if index == 0 or index == '0':
                reference_dict['AdditionalLink'].append(i['link'])
            if index == 1 or index == '1':
                reference_dict['Website'].append(i['link'])
            if index == 3 or index == '3':
                reference_dict['ViewPDF'].append(i['link'])
    except Exception as e:
        pass
        # print('referer= ', e)
    # print('reference_dict= ', reference_dict)
    return reference_dict

def parsePaperContent(parse_index, data):
    """
    解析论文的内容， 其中包括references、cited by、 related
    :return:
    """
    print('=======parseCitedContent=======')
    cited_json = {}
    try:
        papers = data['pr']
        # print('papers= ', papers)

        index = (parse_index - 1) * 10 + 1
        # if parse_index > 0:
        #     index = (parse_index-1) * 10 + 1
        # else:
        #     index = parse_index * 10 + 1
        for paper in papers:
            paper = paper['paper']
            name = paper['dn']
            # 时间
            date = paper['v']['publishedDate']
            displayName = ''
            try:
                displayName = paper['v']['displayName']
            except Exception as e:
                pass
            # 作者信息
            # authors = [author['dn'] for author in paper['a']]
            author_information = {}
            author_index = 1
            for information in paper['a']:
                author_name = information['dn']
                author_sources = information['i']
                temp_list = []
                temp_dict = {}
                for author in author_sources:
                    author_source = ''
                    try:
                        author_source = author['dn']
                    except Exception as e:
                        pass
                    temp_list.append(author_source)
                temp_dict[str(author_index)] = {
                    'author_name': author_name,
                    'author_source': temp_list
                }
                author_index += 1
                author_information.update(temp_dict)

            # 标签
            tags = [tag['dn'] for tag in paper['fos']]

            datasetInformation = ''
            try:
                datasetInformation = paper['d']
            except Exception as e:
                pass
                # print(e)
            cited_id = ''
            try:
                cited_id = paper['id']
            except:
                pass
            citations = ''
            try:
                citations = paper['eccnt']
            except:
                pass
            data_dict = {
                'name': name,
                'date': date,
                'displayName': displayName,
                'authors': author_information,
                'tags': tags,
                'datasetInformation': datasetInformation,
                'id': cited_id,
                'citations': citations
            }
            cited_json[str(index)] = data_dict
            index += 1
    except Exception as e:
        pass
    # print(cited_json)
    return cited_json


def getReferencesData(references_num, page_dict, headers, url, request_data):
    """
    获取references的数据
    :return:
    """
    references_jsondata = {}
    # 将个数转换成页数
    references_nums = references_num // 10
    references_nums_ys = references_num % 10
    if references_nums_ys > 0:
        references_nums += 1

    for i in range(1, references_nums):
    # for i in range(1, 3):
        skip = (i - 1) * 10
        request_data['skip'] = skip
        headers[
            'Referer'] = 'https://academic.microsoft.com/paper/{}/reference/search?q={}&qe={}&f=&orderBy=0&skip={}&take=10'.format(
            page_dict['id'], page_dict['name'], request_data['queryExpression'], skip)
        temp_references_dict = parseNextPage(url, headers, request_data, i)
        references_jsondata.update(temp_references_dict)
    return references_jsondata


def getCitedByData(cited_num, page_dict, headers, url, cited_data):
    """
    得到cited by 的数据
    :return:
    """
    cited_jsondata = {}

    cited_nums = cited_num // 10
    cited_nums_ys = cited_num % 10
    if cited_nums_ys > 0:
        cited_nums += 1

    for i in range(cited_nums):
    # for i in range(1, 4):
        skip = (i - 1) * 10
        cited_data['skip'] = skip
        headers[
            'Referer'] = 'https://academic.microsoft.com/paper/{}/citedby/search?q={}&qe=RId%3D{}&f=&orderBy=0&skip={}&take=10'.format(
            page_dict['id'], page_dict['name'], page_dict['id'], skip)
        temp_cited_dict = parseNextPage(url, headers, cited_data, i)
        cited_jsondata.update(temp_cited_dict)
    return cited_jsondata


def getRelatedData(related_pages, related_data, page_dict, headers, url, relatedPaperExpression):
    """
    获取related的数据
    :return:
    """
    related_jsondata = {}
    for i in range(1, related_pages + 1):
        skip = (i - 1) * 10
        related_data['skip'] = skip
        related_data['queryExpression'] = relatedPaperExpression
        # headers = self.headers
        headers[
            'Referer'] = 'https://academic.microsoft.com/paper/{}/related/search?q={}&qe={}&f=&orderBy=0&skip={}&take=10'.format(
            page_dict['id'], page_dict['name'], relatedPaperExpression, skip)
        temp_related_dict = parseNextPage(url, headers, related_data, i)
        related_jsondata.update(temp_related_dict)
    return related_jsondata
