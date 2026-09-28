<div align="center">
  <img src="./logo.png" alt="fontseca.dev's logo"/>

---

  <a href="https://golang.org/doc/go1.23">
    <img alt="golang version" src="https://img.shields.io/badge/Go-1.23-blue.svg" />
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img alt="project license" src="https://img.shields.io/badge/license-MIT-brightgreen.svg" />
  </a>
  <img alt="last commit" src="https://img.shields.io/github/last-commit/fontseca/fontseca.dev?color=61dfc6&label=last%20commit" />
</div>

Welcome to the source code of my personal website, [fontseca.dev](https://fontseca.dev/). This site is a dedicated
portal where I share my work, experience, ideas, interests, and thoughts. The project represents the culmination of four
years of strong desired to have a place of my own, and one year of devoted work to make it possible. The initial design
was just a single info page about myself, but it eventually turned into a more complete and complex
platform.

One of my favorite sections in the site is *[the archive](https://fontseca.dev/archive/)*.
Before starting the web, I faced a dilemma: use an existing
platform like Hugo, or create a blog manager myself from scratch.
After some thinking, I chose to build my own blog manager—what I decided to call _the archive_.
Here, I address subjects I find interesting and worth sharing. As other sections of the site, the archive is fully
managed through an RPC-like API that powers the content,
and constitutes one of the core parts of my website, alongside my [playground](https://fontseca.dev/playground/). In
this archive, I discuss certain [topics](https://fontseca.dev/playground?target=/archive.topics.list) that interest me.

As a back-end engineer, I encountered a problem most of us have suffered when we want to have a website to present
our work.
When we work on APIs, we often want to showcase some of our labor.
We could talk about it in a detailed article, but most of the time we want to play around with the product.
That is why
I created the second cornerstone of my website—what I call *[the playground](https://fontseca.dev/playground/)*; which
is, by the
way, [open source](https://github.com/fontseca/playground/) and available for integration into other projects.

<div align="center" style="display: flex; justify-content: center; text-align: center;">
  <a href="https://youtu.be/NCcJdYM-UOo" target="_blank">
    <img src="https://markdown-videos-api.jorgenkh.no/youtube/NCcJdYM-UOo" alt="cheerfully celebrating the launch of my personal website built with go 1.23 — fontseca.dev" width="70%">
  </a>
    <p class="text-align: center;"><i>cheerfully celebrating the launch of my personal website built with go 1.23 — fontseca.dev</i></p>
</div>

## Table of Contents

<!-- TOC -->

* [Table of Contents](#table-of-contents)
* [The Archive](#the-archive)
    * [Articles Lifecycle](#articles-lifecycle)
* [The Playground](#the-playground)
* [API Reference](#api-reference)
    * [Errors](#errors)
        * [`internal`](#internal)
        * [`missing_argument`](#missing_argument)
        * [`unparseable_value`](#unparseable_value)
        * [`not_found`](#not_found)
        * [`out_of_range`](#out_of_range)
        * [`unmet_validation`](#unmet_validation)
        * [`duplicate_key`](#duplicate_key)
        * [`action_already_completed`](#action_already_completed)
        * [`action_refused`](#action_refused)
    * [Me](#me)
        * [`me.get`](#meget)
        * [`me.set`](#meset)
        * [`me.set_photo`](#meset_photo)
        * [`me.set_resume`](#meset_resume)
        * [`me.set_hireable`](#meset_hireable)
    * [Experience](#experience)
        * [`me.experience.list`](#meexperiencelist)
        * [`me.experience.hidden.list`](#meexperiencehiddenlist)
        * [`me.experience.get`](#meexperienceget)
        * [`me.experience.create`](#meexperiencecreate)
        * [`me.experience.set`](#meexperienceset)
        * [`me.experience.hide`](#meexperiencehide)
        * [`me.experience.show`](#

[...截断...]

meexperienceshow)
        * [`me.experience.quit`](#meexperiencequit)
        * [`me.experience.remove`](#meexperienceremove)
    * [Projects](#projects)
        * [`me.projects.list`](#meprojectslist)
        * [`me.projects.get`](#meprojectsget)
        * [`me.projects.archived.list`](#meprojectsarchivedlist)
        * [`me.projects.create`](#meprojectscreate)
        * [`me.projects.set`](#meprojectsset)
        * [`me.projects.archive`](#meprojectsarchive)
        * [`me.projects.unarchive`](#meprojectsunarchive)
        * [`me.projects.finish`](#meprojectsfinish)
        * [`me.projects.unfinish`](#meprojectsunfinish)
        * [`me.projects.remove`](#meprojectsremove)
        * [`me.projects.set_playground_url`](#meprojectsset_playground_url)
        * [`me.projects.set_first_image_url`](#meprojectsset_first_image_url)
        * [`me.projects.set_second_image_url`](#meprojectsset_second_image_url)
        * [`me.projects.set_github_url`](#meprojectsset_github_url)
        * [`me.projects.set_collection_url`](#meprojectsset_collection_url)
        * [`me.projects.technologies.add`](#meprojectstechnologiesadd)
        * [`me.projects.technologies.remove`](#meprojectstechnologiesremove)
    * [Project Technology Tags](#project-technology-tags)
        * [`technologies.list`](#technologieslist)
        * [`technologies.create`](#technologiescreate)
        * [`technologies.set`](#technologiesset)
        * [`technologies.remove`](#technologiesremove)
    * [Archive Article Drafts](#archive-article-drafts)
        * [`archive.drafts.start`](#archivedraftsstart)
        * [`archive.drafts.publish`](#archivedraftspublish)
        * [`archive.drafts.list`](#archivedraftslist)
        * [`archive.drafts.get`](#archivedraftsget)
        * [`archive.drafts.share`](#archivedraftsshare)
        * [`archive.drafts.revise`](#archivedraftsrevise)
        * [`archive.drafts.discard`](#archivedraftsdiscard)
        * [`archive.drafts.tags.add`](#archivedraftstagsadd)
        * [`archive.drafts.tags.remove`](#archivedraftstagsremove)
    * [Archive Articles](#archive-articles)
        * [`archive.articles.list`](#archivearticleslist)
        * [`archive.articles.get`](#archivearticlesget)
        * [`archive.articles.hidden.list`](#archivearticleshiddenlist)
        * [`archive.articles.amend`](#archivearticlesamend)
        * [`archive.articles.set_slug`](#archivearticlesset_slug)
        * [`archive.articles.hide`](#archivearticleshide)
        * [`archive.articles.show`](#archivearticlesshow)
        * [`archive.articles.remove`](#archivearticlesremove)
        * [`archive.articles.pin`](#archivearticlespin)
        * [`archive.articles.unpin`](#archivearticlesunpin)
        * [`archive.articles.tags.add`](#archivearticlestagsadd)
        * [`archive.articles.tags.remove`](#archivearticlestagsremove)
    * [Archive Article Patches](#archive-article-patches)
        * [`archive.articles.patches.list`](#archivearticlespatcheslist)
        * [`archive.articles.patches.revise`](#archivearticlespatchesrevise)
        * [`archive.articles.patches.share`](#archivearticlespatchesshare)
        * [`archive.articles.patches.discard`](#archivearticlespatchesdiscard)
        * [`archive.articles.patches.release`](#archivearticlespatchesrelease)
    * [Archive Tags](#archive-tags)
        * [`archive.tags.create`](#archivetagscreate)
        * [`archive.tags.list`](#archivetagslist)
        * [`archive.tags.set`](#archivetagsset)
        * [`archive.tags.remove`](#archivetagsremove)
    * [Archive Topics](#archive-topics)
        * [`archive.topics.create`](#archivetopicscreate)
        * [`archive.topics.list`](#archivetopicslist)
        * [`archive.topics.set`](#archivetopicsset)
        * [`archive.topics.remove`](#archivetopicsremove)

<!-- TOC -->

## The Archive

<figure>
  <img src="https://github.com/user-attachments/assets/74955b4d-42c2-4d2c-b7f1-25a4d07e1c5d" alt="archive"/>
  <figcaption>
    <p><i>A screenshot of the fontseca.dev's arch