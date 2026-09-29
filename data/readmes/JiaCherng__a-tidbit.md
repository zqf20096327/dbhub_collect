# What is Happening by Jack
## Website URL: https://jiacherng.github.io/what-is-happening/
#### Video Demo:  https://youtu.be/nZtDJaghuAY
#### Description:

Set up a blog using Jekyll with Github pages.

I have been writing letters and comments to be submitted and published by mainstream online news media in my country, Malaysia. With the opportunity provided by CS50,
I thought it would be a good opportunity to have a central site where I can collect the articles I have written.

After considering a few sites as host, github pages was my choice for its straighforward interface and less clutter (less things, accounts to connect to). With that I
was introduce to Jekyll.

1. Developed the project on my local pc, not CS50 ide. Used wsl2 on vscode.
2. Followed [Jekyll](https://jekyllrb.com/) step by step tutorial to set up a basic jekyll webpage
3. Wanted to style my site from scratch, but realied it was too much hassle and requires more in depth knowledge of css(and associated library) that it would
   take too much effort and time. Went to search for themes develop, settles on [sleek](https://github.com/janczizikow/sleek).
4. Instead of building my site from the themes, I migrated (copy and paste) the layouts and include folders that I wanted.
5. Faced a problem with loading pages and its features as github pages has an additional baseurl on top of the site url, pages loads on local host but not on gh-pages.
   Found solution using relative_url folder and #baseurl(comment out) in _config.yml, gh=pages will configure baseurl automatically.
6. Theme used does not have a dropdown navigation bar. Used bootstrap to implement navbar in _includes/header.html .
7. Using categories function on Jekyll, iterated over different categories for different dropdown meny via Django in _includes/header.html for navbar.
8. Discovered that my menu has different style than that of the template. Read through assets/css/main.css. To search out relevant classes and add it to my own menu.
9. Learned basics of markdown,GFM to edit my articles to post them on my blog.
10. Throughout the process, used many git commands and was able to be more familiar with git. In particular, the branch and reset version was found to be extremely useful.
11. Tried to set up a page that wasn't the index page using permalink as .../index.html/, while the home/index page remain as .../. It did not work as .../ loads index.html instead.
    Most likely a system default that loads index.html as the default page whenever we visit the naked page url. Had to change index.html to menu.html.

#### Conclusion: 
Project has less coding but a lot of small problems cropped out along the way. Understood the complexities of coding along with the many nuances, small errors that
are hard to pick up. Was introduced to many languages such as Ruby, scss, markdown, and yml.

