# Funstall

This is my own custom package manager (well, mostly it's a wrapper around other
package managers).

## Usage

### List all available packages

```sh
funstall list
```

## Why?

I use multiple operating systems on multiple machines, requiring me to switch
between package managers (mainly pacman and brew).
My goal is to have a consistent, personal workflow no matter which machine I
use, so I need a wrapper around platform-specific package managers.

As a side note, I also don't agree with how some AUR packages are implemented,
so I'm hesitant to use `yay` on Arch.
Implementing my own installation scripts based on AUR implementations also
makes me feel safer from supply-chain attacks.

## Implementation Considerations

Initially I planned to implement this in nushell within my dotfiles.
However I started to feel uneasy with the rather simplistic typing system in
nushell as data models surpassed a certain level of complexity.
Therefore I decided to reach for another programming language.

I started this project using Python because I want to avoid writing a GitHub
action for now to distribute this project across my computers.
Generally I prefer compiled languages for CLI applications though so I may
**rewrite in Rust™** in the future (or in another language).

## Development

Publish a new version:

First create a PyPI API key with access to the repository.
Then save it in `.pypi-token.secret`.

```sh
uv build --sdist
uv publish --token $(cat .pypi-token.secret)
```
