# Federated Learning Resources

[![Stars](https://img.shields.io/github/stars/youngfish42/Awesome-FL.svg?color=orange)](https://github.com/youngfish42/Awesome-FL/stargazers) [![Awesome](https://awesome.re/badge-flat.svg)](https://awesome.re) [![License](https://img.shields.io/github/license/youngfish42/Awesome-FL.svg?color=green)](https://github.com/youngfish42/image-registration-resources/blob/master/LICENSE) ![](https://img.shields.io/github/last-commit/youngfish42/Awesome-FL) 

---

**Table of Contents**

- [Papers](#papers)
  - [FL in top-tier journal](#fl-in-top-tier-journal)
  - FL in top-tier conference and journal by category
    - [AI](#fl-in-top-ai-conference-and-journal) [ML](#fl-in-top-ml-conference-and-journal) [DM](#fl-in-top-dm-conference-and-journal) [Secure](#fl-in-top-secure-conference-and-journal) [CV](#fl-in-top-cv-conference-and-journal) [NLP](#fl-in-top-nlp-conference-and-journal) [IR](#fl-in-top-ir-conference-and-journal) [DB](#fl-in-top-db-conference-and-journal) [Network](#fl-in-top-network-conference-and-journal) [System](#fl-in-top-system-conference-and-journal) [Others](#fl-in-top-conference-and-journal-other-fields)
  - [FL on Graph Data and Graph Neural Networks](#fl-on-graph-data-and-graph-neural-networks) [[dblp]](https://dblp.uni-trier.de/search?q=Federated%20graph%7Csubgraph%7Cgnn) 
  - [FL on Tabular Data](#fl-on-tabular-data) [[dblp]](https://dblp.org/search?q=federate%20tree%7Cboost%7Cbagging%7Cgbdt%7Ctabular%7Cforest%7CXGBoost)
- [Framework](#framework)
- [Datasets](#datasets)
- [Surveys](#surveys)
- [Tutorials and Courses](#tutorials-and-courses)
- Key Conferences/Workshops/Journals
  - [Workshops](#workshops) [Special Issues](#journal-special-issues) [Special Tracks](#conference-special-tracks)
- [Update log](#update-log)
- [Acknowledgments](#acknowledgments)
- [Citation](#citation)



We use another project to automatically track updates to FL papers, click on [FL-paper-update-tracker](https://github.com/youngfish42/FL-paper-update-tracker) if you need it.

Please note that if this page does not display the full content, **please visit [the official homepage](https://youngfish42.github.io/Awesome-FL) for full information.**

**More items will be added to the repository**. Please feel free to suggest other key resources by opening an [issue](https://github.com/youngfish42/Awesome-FL/issues) report, submitting a pull request, or dropping me an email @ ([im.young@foxmail.com](mailto:im.young@foxmail.com)). If you want to communicate with more friends in the field of federated learning, please join the QQ group [联邦学习交流群], the group number is 833638275. Enjoy reading!



**Repository Update Notice** 

> 2024/09/30
>
> 
>
> Dear Users, We would like to inform you of a few changes that will affect this open source repository. The owner and principal contributor [@youngfish42](https://github.com/youngfish42) has successfully completed his doctoral studies 🎓 as of September 30, 2024, and has since shifted his research focus. This change in circumstances will impact the frequency and extent of updates to the repository's paper list. 
>
> Instead of the previous regular updates, we anticipate that the paper list will now be updated on a monthly or quarterly basis. Furthermore, the depth of these updates will be reduced. For instance, updates related to the author's institution and open source code will no longer be actively maintained. 
>
> We understand that this might affect the value you derive from this repository. Therefore, we humbly invite more contributors to participate in updating the content. This collaborative effort will ensure that the repository remains a valuable resource for everyone. 
>
> We appreciate your understanding and look forward to your continued support and contributions. 
>
> 
>
> Best Regards, 
>
> 白小鱼 (youngfish)
>




# papers

**categories**

- Artificial Intelligence (IJCAI, AAAI, AISTATS, ALT, AI)

- Machine Learning (NeurIPS, ICML, ICLR, COLT, UAI, Machine Learn

[...截断...]

ing, JMLR, TPAMI)

- Data Mining (KDD, WSDM)

- Secure (S&P, CCS, USENIX Security, NDSS)

- Computer Vision (ICCV, CVPR, ECCV, MM, IJCV)

- Natural Language Processing (ACL, EMNLP, NAACL, COLING)

- Information Retrieval (SIGIR)

- Database (SIGMOD, ICDE, VLDB)

- Network (SIGCOMM, INFOCOM, MOBICOM, NSDI, WWW)

- System (OSDI, SOSP, ISCA, MLSys, EuroSys, TPDS, DAC, TOCS, TOS, TCAD, TC) 

- Others (ICSE, FOCS, STOC)




<details open>
<summary> Events </summary>

| Venue                                                        | 2024-2020                                                    | before 2020                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| [IJCAI](https://dblp.uni-trier.de/search?q=federate%20venue%3AIJCAI%3A) | [25](https://www.ijcai.org/proceedings/2025/), [24](https://www.ijcai.org/proceedings/2024/), [23](https://www.ijcai.org/proceedings/2023/), [22](https://www.ijcai.org/proceedings/2022/), [21](https://www.ijcai.org/proceedings/2021/), [20](https://www.ijcai.org/proceedings/2020/) | [19](https://www.ijcai.org/proceedings/2019/)                |
| [AAAI](https://dblp.uni-trier.de/search?q=federate%20venue%3AAAAI%3A) | [26](https://dblp.org/db/conf/aaai/aaai2026.html), [25](https://dblp.org/db/conf/aaai/aaai2025.html), [24](https://dblp.org/db/conf/aaai/aaai2024.html), [23](https://dblp.org/db/conf/aaai/aaai2023), [22](https://aaai.org/Conferences/AAAI-22/wp-content/uploads/2021/12/AAAI-22_Accepted_Paper_List_Main_Technical_Track.pdf), [21](https://aaai.org/Conferences/AAAI-21/wp-content/uploads/2020/12/AAAI-21_Accepted-Paper-List.Main_.Technical.Track_.pdf), [20](https://aaai.org/Conferences/AAAI-20/wp-content/uploads/2020/01/AAAI-20-Accepted-Paper-List.pdf) | -                                                            |
| [AISTATS](https://dblp.uni-trier.de/search?q=federate%20venue%3AAISTATS%3A) | [25](https://proceedings.mlr.press/v258/), [24](http://proceedings.mlr.press/v238/), [23](http://proceedings.mlr.press/v206/), [22](http://proceedings.mlr.press/v151/), [21](http://proceedings.mlr.press/v130/), [20](http://proceedings.mlr.press/v108/) | -                                                            |
| [ALT](https://dblp.uni-trier.de/search?q=federate%20streamid%3Aconf%2Falt%3A) | 22                                                           | -                                                            |
| [AI](https://dblp.uni-trier.de/search?q=federate%20streamid%3Ajournals%2Fai%3A) (J) | 26, 25, 23                                                   | -                                                            |
| [NeurIPS](https://dblp.uni-trier.de/search?q=federate%20venue%3ANeurIPS%3A) | [24](https://openreview.net/group?id=NeurIPS.cc/2024/Conference#tab-accept-oral), [23](https://openreview.net/group?id=NeurIPS.cc/2023/Conference#tab-accept-oral), [22](https://papers.nips.cc/paper_files/paper/2022), [21](https://papers.nips.cc/paper/2021), [20](https://papers.nips.cc/paper/2020) | [18](https://papers.nips.cc/paper/2018), [17](https://papers.nips.cc/paper/17) |
| [ICML](https://dblp.uni-trier.de/search?q=federate%20venue%3AICML%3A) | [25](https://icml.cc/Conferences/2025/Schedule?type=Poster), [24](https://icml.cc/Conferences/2024/Schedule?type=Poster), [23](https://icml.cc/Conferences/2023/Schedule?type=Poster), [22](https://icml.cc/Conferences/2022/Schedule?type=Poster), [21](https://icml.cc/Conferences/2021/Schedule?type=Poster), [20](https://icml.cc/Conferences/2020/Schedule?type=Poster) | [19](https://icml.cc/Conferences/2019/Schedule?type=Poster)  |
| [ICLR](https://dblp.uni-trier.de/search?q=federate%20venue%3AICLR%3A) | [25](https://openreview.net/group?id=ICLR.cc/2025), [24](https://openreview.net/group?id=ICLR.cc/2024/Conference), [23](https://openreview.net/group?id=ICLR.cc/2023/Conference), [22