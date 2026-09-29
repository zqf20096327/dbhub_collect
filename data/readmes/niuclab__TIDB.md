# TIDB

Trained immunity, referred as innate immune memory, is an emerging new property that describ-ing innate immune system also exhibits augmented immune response to a secondary stimulus. Accumulating evidence reveals that trained immunity not only has broad benefits to host defense but also harmful to host in chronic inflammatory diseases. Trained immunity plays an important role in host defense and immune-mediated diseases. However, all trained immunity-related in-formation is scattered in the literature. 

Here, we describe TIDB, a comprehensive database that provides well-studied trained immunity-related genes in human, rat or mouse as well as the evi-dence in literature. Moreover, TIDB also provides three modules to analyze and invest the func-tion of the trained-immunity-related genes of interest, including Reactome pathway over-representation analysis, Gene Ontology (GO) enrichment analysis and protein-protein interaction (PPI) subnetwork reconstruction. TIDB database will be useful to provide a valuable strategy for vaccine designing and immunity-mediated disease therapy.

### Dependences

- [MongoDB](https://www.mongodb.com/try/download/community), database server
- [node.js](https://nodejs.org/)
- [egg](https://eggjs.org/)

### data import

```sh
mongorestore --archive=TIDB_api/data/tidb.dump
```

### Development

```bash
$ npm i
$ npm run dev
$ open http://localhost:7001/
```

### Deploy

```bash
$ npm start
$ npm stop
```

 Your suggestion and contribution well be highly appreciated. Please feel free 
 to [contact me](mailto:yiluheihei@gmail.com) if you have any questions.
