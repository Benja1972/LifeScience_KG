# KG construction

### Intro

We use CURIEs identifiers <https://en.wikipedia.org/wiki/CURIE>. They can be resolved in <https://identifiers.org/> - The *Identifiers.org* Resolution Service provides consistent access to life science data using Compact Identifiers. (TODO: alternative <https://bioregistry.io/>)

Glossary

-   **id** - Primary reference

-   **labels** - type of entity

-   **xref** - Secondary refs for linking etc

-   **tui** - UMLS semantic type codes

-   **cui** - UMLS codes

-   **umls_sty** - UMLS semantic type literal

### Ontologies

Ontology is used to classify entities. In BioMedical domains there are long list of well-known and curated ontologies. We select one ontology per entity type as primary ontology for these entity.

-   ATC - ontology for chemical compounds. The Anatomical Therapeutic Chemical (ATC) Classification System is used for the classification of active ingredients of drugs according to the organ or system on which they act and their therapeutic, pharmacological and chemical properties. It is controlled by the World Health Organization Collaborating Centre for Drug Statistics Methodology (WHOCC)

    -   id ATC:ID

    -   labels (type) - ATC_term

    -   name

    -   tui

    -   cui

    -   umls_sty

    -   data <https://bioportal.bioontology.org/ontologies/ATC>

-   MeSH - mixed ontology of bio-medical terms, chemical compounds, diseases etc.

    -   id - MESH:ID

    -   labels - MESH_term

    -   name

    -   tui

    -   cui

    -   umls_sty

    -   data <https://bioportal.bioontology.org/ontologies/MESH>

-   DOID - Disease. The Disease Ontology has been developed as a standardized ontology for human disease with the purpose of providing the biomedical community with consistent, reusable and sustainable descriptions of human disease terms, phenotype characteristics and related medical vocabulary disease concepts through collaborative efforts of biomedical researchers, coordinated by the University of Maryland School of Medicine, Institute for Genome Sciences. The Disease Ontology semantically integrates disease and medical vocabularies through extensive cross mapping of DO terms to MeSH, ICD, NCI's thesaurus, SNOMED and OMIM.

    -   id DOID:ID - <https://disease-ontology.org/>

    -   xref

    -   name

    -   data - CKG

### Entities

List of datasets containing entity instances (metadata) and information on relationships, interactions etc., between entities.

-   Companies - FDA's companies

    -   id - DUNS:ID <https://www.fdahelp.us/fda-establishment-registration-ndc-labeler-code-number.html>

    -   xref - ?

    -   name

    -   data

        -   <https://www.fda.gov/drugs/drug-approvals-and-databases/drug-establishments-current-registration-site>

        -   <https://www.accessdata.fda.gov/scripts/cder/wdd3plreporting/index.cfm>

        -   <https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/annual-reporting-prescription-drug-wholesale-distributors-and-third-party-logistics-providers>

            -   <https://www.fda.gov/about-fda/ethics/listing-significantly-regulated-organizations-sro>

            -   <https://www.accessdata.fda.gov/scripts/sda/sdNavigation.cfm?sd=srolist&displayAll=false&page=1>

            -   <https://www.fda.gov/medical-devices/device-registration-and-listing/establishment-registration-and-medical-device-listing-files-download>

-   Drug_product(labels)

    -   id NDC:ID - National Drug Code (NDC) which serves as the FDA's identifier for drugs

        -   <https://www.fda.gov/drugs/drug-approvals-and-databases/approved-drug-products-therapeutic-equivalence-evaluations-orange-book>

        -   <https://www.fda.gov/drugs/drug-approvals-and-databases/national-drug-code-directory>

    -   xref

    -   name

    -   data - see Companies entities

-   Chemical compound

    -   id PubChem.Compound:ID - PubChem ID - <https://pubchem.ncbi.nlm.nih.gov/>

    -   xref UNII ID <https://fdasis.nlm.nih.gov/srs/jsp/srs/uniiListDownload.jsp>

    -   name

    -   data

        -   rxnorm_mapping <https://dailymed.nlm.nih.gov/dailymed/spl-resources-all-mapping-files.cfm>

-   Genes

    -   id - HGNC <https://www.genenames.org/>

    -   xref

    -   name

    -   data - CKG

-   Proteins

    -   id - UniProt <https://www.uniprot.org/>

    -   xref

    -   name

    -   data - CKG

-   Med Devices

    -   id - 510(K) Number ID

    -   xref

    -   name

    -   data

-   ClinicalTrials

    -   id clinicaltrials:ID (https://registry.identifiers.org/registry/clinicaltrials)

    -   name

    -   data

        -   https://aact.ctti-clinicaltrials.org/ - Database (Postgres)

        -   https://aact.ctti-clinicaltrials.org/schema - Schema

-   Disease

    -   id DOID:ID - <https://disease-ontology.org/>

    -   xref

    -   name

    -   data - CKG

-   Vaccines

    -   id Vaccines are part of Drug_product

    -   xref

    -   name

    -   data

-   Patents

    -   data <https://www.surechembl.org/search/> - Patents annotated by chemical compounds

### Relationships

### Output format

Output format is presented as table where specifically defined columns names and name of table help to process data in connected graph. All processed tables could be pushed to graph construction script and KG will be built automatically.

::: centering
![Example of table for entities](EntityTable.svg){#fig:Example-of-table}
:::

-   *Drug_product.csv* - Table name is exact Entity type

-   *ID,Product_type,Application_number* - simple columns names - metadata for node

-   *REL:has_ingredient -* column starts with *REL:* is for outgoing relations with name of relation after ":" It contains list of IDs of entities to be linked with entity in registry (current line) (*n*)-\[*has_ingredien*t\]-\>(*m*)

-   *LER:manufactures* *-* column starts with *LER:* is for incoming relations with name of relation after ":" It contains list of IDs of entities to be linked with entity in registry (current line) (*n*)\<-\[*manufactures*\]-(*m*)

Example of table is presented in Fig. [1](#fig:Example-of-table){reference-type="ref" reference="fig:Example-of-table"}

Final Knowledge Graph is presented on Fig. [2](#fig:Graph){reference-type="ref" reference="fig:Graph"}

::: centering
![Graph](GraphExample.svg)
:::

# Data Review

### Ontology/Semantic type (probable)

-   https://lhncbc.nlm.nih.gov/semanticnetwork/

-   https://bioportal.bioontology.org/

### Genes

-   https://www.ncbi.nlm.nih.gov/gene?cmd=Retrieve&dopt

-   https://www.ensembl.org/index.html

### Proteins

-   https://www.uniprot.org/

### Compounds 

#### Drugs

-   https://pubchemdocs.ncbi.nlm.nih.gov/statistics

-   https://bioportal.bioontology.org/ontologies/ATC/

-   https://www.ebi.ac.uk/chembl/

-   FDA resources

    -   https://www.fda.gov/drugs

    -   https://fda.report/

    -   https://open.fda.gov/

    -   https://dailymed.nlm.nih.gov/dailymed/index.cfm

    -   https://www.accessdata.fda.gov/scripts/cder/daf/ - Approved drugs

    -   https://www.altexsoft.com/blog/drug-data-openfda-dailymed-rxnorm-goodrx/ list of APIs to Drug databases

-   https://drugcentral.org/

-   EMA

    -   https://www.ema.europa.eu/en

    -   https://ec.europa.eu/health/documents/community-register/html/reg_hum_atc.htm - Centralised medicinal products for human use by ATC code

-   https://www.kegg.jp/kegg/drug/ - KEGG DRUG is a comprehensive drug information resource for approved drugs in Japan, USA and Europe, unified based on the chemical structure and/or the chemical component of active ingredients.

#### Biologics

Vaccines, blood and tissue products, and biotechnology. New biologics are required to go through a premarket approval process called a Biologics License Application (BLA), similar to that for drugs.

-   https://www.fda.gov/vaccines-blood-biologics

#### Product

-   https://go.drugbank.com/

-   https://www.accessdata.fda.gov/scripts/cder/daf/ - Approved drugs

### Medical Devices

-   https://www.fda.gov/medical-devices

-   https://bioportal.bioontology.org/ontologies/SNOMEDCT

-   https://bioportal.bioontology.org/ontologies/MESH

### Food

-   https://www.fda.gov/food - Food and dietary supplements

### Diseases

-   https://www.ebi.ac.uk/efo/

-   https://www.ebi.ac.uk/ols/ontologies/mondo

-   https://www.ebi.ac.uk/ols/ontologies/doid

-   https://www.nlm.nih.gov/mesh/meshhome.html

-   https://icd.who.int/en

-   https://www.ebi.ac.uk/ols/ontologies/ncit

### Pathways 

-   https://reactome.org/what-is-reactome

### Clinical Trials

-   NIH (clinicaltrials.gov, data dump - https://aact.ctti-clinicaltrials.org/)

-   EU Clinical Trials Register (clinicaltrialsregister.eu) (https://eudract.ema.europa.eu/)

-   WHO International (https://www.who.int/clinical-trials-registry-platform)

### Patents

-   https://www.surechembl.org/

-   http://www.almaden.ibm.com/

-   https://patentscope.wipo.int/

### Intearactions

-   Drug --\> Drug: https://mor.nlm.nih.gov/RxNav/

-   Chemicals -\> Proteins http://stitch.embl.de/

### Combo

-   https://www.opentargets.org/

-   https://pharos.nih.gov/about

### APIs

-   https://biothings.io/

-   http://mychem.info/

### Knowledge Graphs

-   https://github.com/callahantiff/PheKnowLator - https://youtu.be/uNAFd6GgwGE

-   https://github.com/gnn4dr/DRKG

-   https://github.com/MannLabs/CKG

-   https://het.io/

-   https://github.com/Knowledge-Graph-Hub/kg-covid-19

-   https://github.com/dsi-bdi/biokg

-   https://monarchinitiative.org/

-   https://github.com/MindRank-Biotech/PharmKG

-   https://github.com/OpenBioLink/OpenBioLink

-   https://data.mendeley.com/datasets/mrcf7f4tc2/1

### Notes

L-.1667em.25emY-.125emX LaTeX

#### Elsevier Biology KG

    Entity type Quantity
    Cell    4,181
    Cell object 609
    Cell process    14,906
    Clinical parameter  5,284
    Disease 22,433
    Genetic Variant 157,344
    Small molecule (drug)   1,057,236
    Protein/gene    141,779
    Complex 992
    Functional class    5,485
    Organ   3,857
    Tissue  579
    Virus   25,287
    Treatment   82
    Total   1,440,054

