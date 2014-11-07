## sagarpandya.com

This is the repo where I store my statically generated website. It's built using [middleman](http://middlemanapp.com/), a static site generator and templating engine written in Ruby.

`middleman/sagarpandya.com/source/` is where the site itself lives, and `hooks` contains the local git hooks for this repository. Performing a `git push` will instruct `middleman` to build the static site, and then copy it to my server at [sagarpandya.com].

Symlink the `hooks/` directory into `.git/hooks` to get the upload functionality working:

```bash
$ cd .git
$ ln -s ../hooks .
```
