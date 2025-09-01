# <img src="./images/logo.png" width="30"> ChartsGouv : L'outil de visualisation de données de l'État  

> AVERTISSEMENT : Ce système de conception est uniquement destiné à être utilisé pour les sites web officiels des services publics français.
> Son objectif principal est de faciliter l'identification des sites gouvernementaux par les citoyens. [Voir les conditions](https://www.systeme-de-design.gouv.fr/utilisation-et-organisation/perimetre-d-application).

## Contexte
Ce projet est né d'un constat simple: il existe une multitude d'outils propriétaires au sein de l'État, ce qui complique la montée en compétence des agents, empêche la revaloration de leurs compétences auprès d'autres administrations et rend difficile la mutualisation des connaissances.  

Ce projet a été inité par l'intermédiaire du [programme 10%](https://www.10pourcent.etalab.gouv.fr/), programme interministériel co-porté par la DINUM et l'INSEE. Il a permis à plusieurs agents de différentes administrations de collaborer sur leurs problématiques communes.

## Cliquer pour voir le résultat en vidéo
<a href="https://www.youtube.com/watch?v=0o1JbSbwoM8" title="Regarder sur YouTube">
    <img src="/images/demo_graphes_echarts.png" width="750" alt="Regarder sur YouTube">
</a>

## Parcourir les dashboards d'exemple
- [Dashboard SILL](http://chartsgouv.lab.sspcloud.fr/superset/dashboard/sill/)
- [Graphes Apache Echarts avec couleurs DSFR](http://chartsgouv.lab.sspcloud.fr/superset/dashboard/demo-echarts/)
- [Composants DSFR et DSFR charts](http://chartsgouv.lab.sspcloud.fr/superset/dashboard/demo-dsfr/?standalone=2)


  
## Description
> [!IMPORTANT]  
> Ce projet n'est pas un fork du repo officiel de Superset.  

Ce projet est une extension du projet Superset. Il vise à compléter cet outil en y intégrant la couche DSFR de l'État. Il a aussi vocation à expérimenter des fonctionnalités spécifiques propres aux besoins des administrations et aux utilisateurs francophones de cet outils.

### Accès rapides
- :art: [Personnalisation](./superset/)
- [Deploiement avec Docker](./docs/docker.md)
- [Deploiement avec Helm](./docs/helm.md)

### Prise en main
Une documentation en français d'Apache Superset a été rédigée par le MTE.  
Pour la consulter, rendez-vous sur [ce site](https://snum.gitlab-pages.din.developpement-durable.gouv.fr/ds/gd3ia/offre-dataviz-documentation/).  
> [!NOTE]  
> Certains éléments de cette documentation sont propres à l'environnement du MTE.  
> 
Si vous souhaitez y contribuer, vous pouvez trouver des contacts dans la section "A propos" du site

## License
This project is distributed under the EUPL v1.2 license — see the LICENSE file for more details.
