# ComfyUI Scene Composer

A collection of [ComfyUI](https://github.com/comfyanonymous/ComfyUI) nodes to create scenes with random procedural generation.

## Installation

Clone this repo in `custom_nodes`, in your ComfyUI folder.

```shell
$ git clone https://github.com/taches/comfyui-scene-composer
$ pip install -r requirements.txt
```

## Nodes

### Scene

The Scene node generates a procedural random prompt as a string. The prompt follows the following structure:

| Component       | Description                                                   |
| --------------- | ------------------------------------------------------------- |
| **C**omposition | The layout of the scene, cameras, number of protagonists, etc |
| **A**ctions     | Activites done by the character/protagonist(s)                |
| **C**haracter   | Main character, focusing on body type and faces, etc          |
| **C**lothes     | Include casual clothes, uniforms, swimsuits, underwear, etc   |
| **E**nvironment | The setting, including background, weather, time of day, etc  |

You can define some aspects of the scene directly in the node. If you want to have more control over what's generated, you can override these components by passing a string as input. This work particularly well with the node components, which are explained just below.

### Components

Node components also generate a procedural random prompt as a string. It can be used to have better control over the generation of each concept. You can then pass it to the Scene node or even us it as standalone.

### Seed

Each node has its own seed. This way, you can alter the generation of each component independently without changing the whole scene. The scene seed is just there as a fallback if a component is not set in the optional input.

## Config files

You can configure components and other related concepts using the TOML files situated in the `config` folder.

Strings will output the chain of tags as it is. Lists will randomly take one tag

```toml
tags = "foo, bar"     # -> foo, bar
tags = ["foo", "bar"] # -> bar
```

### Weighted lists

You can change the distribution by assigning a `?weight` next to the tag. By default, every tag has a weight of 1.

```toml
tags = ["foo?2", "bar", "baz"]
```

In this example, `foo` has a 50% chance to be chosen over `bar` or `baz`. This is because its weight is 2x the sum of all weights:

$\cfrac{\text{foo}}{\text{foo+bar+baz}} = \cfrac{2}{2+1+1}=0.5$

You can of course add fractions to the weights to make it _less_ likely to be chosen.

```toml
tags = ["foo?0.5", "bar", "baz"]
```

In this example, `foo` has a 20% chance to be chosen over `bar` or `baz`.

### Probabilities and repetitions

Some notations inside config files allow to alter the generation:

- `probability` define how likely the group of tags will be retained
- `repeat` define how many tags should be taken from a list with the key

You can do so by moving the string/list into a dictionary with the `tags` key.

```toml
# Before
[group]
items = ["foo", "bar", "baz"]

# After
[group.items]
probability = 0.75
repeat = 2
tags = ["foo", "bar", "baz"]
```

In this example, there is a 25% chance to ignore the tags. If it's not the case, 2 tags will be chosen from the list.

> [!NOTE]
> You can also determine a range of tags to take from the list.<br>
> For example: `repeat = [2,4]` will take between 2 and 4 tags

### Nested lists

You can define a `list` that includes the name of nested elements. This way, you can set what concept is randomly chosen and how likely.

```toml
[group]
list = ["foo:2", "bar"]
foo = ["tag1", "tag2", "tag3"]
bar = ["tag4", "tag5", "tag6"]
baz = ["tag7", "tag8", "tag9"]
```

In this example, `foo` tags are more likely to be chosen than `bar` tags. `baz` is not included in the `list` and will never be chosen.
