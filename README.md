# Introduction 介绍

This is an experimental music project with the idea of averaging several melodies.

The origin of this experiment lies in a general education chorus class, where the teacher assigned a creative project related to mothers, with no restrictions on content or form. The requirement was to combine this project with our major.

I attend a media university, so most of the students in this course come from arts or humanities backgrounds. They can create recitations, songs, paintings, or literary works. However, my major is Data Science.

What should I do? How can I combine Data Science with a creative project?

After much thought, I came up with this idea: to conduct a music experiment.

I want to use mathematical methods to average several melodies and see what kind of sound this generates. Personally, I find this idea quite novel.

Here's a rough outline of my plan:

- First, collect several pieces of classical music related to mothers and extract their main melodies.
- Use an algorithm to average (or similarly process) these melodies to form a sequence of microtones.
- Process this sequence of microtones, adding some microtonal harmonization to make it sound more pleasant.

这是一个实验音乐项目，想法是平均几段旋律

这个实验的缘由是，在一节合唱通识课上，老师布置了一个内容与形式不限，主题是与母亲有关的创作，其中的要求是要与自己所学专业结合。

我所处的是一所传媒类院校，因此这门课程上多是一些艺术或文史类专业，它们可以做朗诵、歌唱、绘画或者文学的内容，而我的专业却是数据科学。

这该怎么办？怎么结合数据科学创作？

构思了许久，我想到了这样的想法，做一个音乐实验：

我想使用数学的方法对几段旋律进行平均，并想知道这样生成的声音是怎么样的？这个想法我个人还是觉得挺新鲜的

大致梳理了一下思路：

- 首先收集若干首与母亲有关的古典音乐，提取出其主旋律。
- 通过某种算法将这若干个旋律进行平均（或类似的处理），形成一段微分音序列。
- 对这个微分音序列进行处理，加上一定的微分和声编配，使其听起来更加顺耳一点。

# Sources of Music 乐曲来源

1. Brahms' "Lullaby in F Major"

2. Schubert's "Lullaby"

3. Mozart's "Ah vous dirai-je, Maman"

4. Mozart's "Violin Sonata No. 18 in G Major, KV301"

5. Beethoven's "Romance in F Major"

6. Dvořák's "Songs My Mother Taught Me"

1. 勃拉姆斯《F大调摇篮曲》

2. 舒伯特《摇篮曲》

3. 莫扎特《Ah vous dirai-je, Maman》

4. 莫扎特《Violin Sonata No. 18 in G Major, KV301》

5. 贝多芬《F大调浪漫曲》

6. 德沃夏克《母亲教我的歌》

# Main Methods主要方法

## Input and Process data 录入并处理数据

First, I need to explain the data structure. I store different musical phrases in melodies.txt, where each line represents a single phrase.

Each note is saved as a tuple containing its information, such as (X, T), where X represents the pitch and T represents the duration.

The calculation method for X uses A2 as the reference pitch, which has a value of 0. Using the equal temperament system, the value of other notes is determined by their interval from A2. For instance, A#2 has a value of 100. Additionally, a rest is represented with an empty X.

The calculation method for T is note duration / quarter note duration. For example, in 2/4 time, a half note's duration is 2.

首先我需要解释一下数据结构，我将不同的乐句保存在`melodies.txt`中，其中每一行表示一个单独的句子。

每一个音以一个元组保存其信息，例如(X,T)，其中X表示音高，T表示时长。

X的计算方式我以A2为基准，其值为0，采用十二平均律的律制计算其他音和它的音程决定其值，X为该音与A2相差的音分，例如A#2为100。此外规定休止符的X为空。

T的计算方式为`该音时值/四分音符时值`，例如在2/4拍中，一个二分音符的时值为2。

## Normalization 正则化

> The idea here is to stretch multiple musical phrases of varying lengths to make them the same length.

Multiply T for every note in a phrase by the reciprocal of the total length of that phrase.

> 这里的想法是把多个长短不一的乐句拉伸，使长度相同。

将所有一个乐句内所有音的T乘以其乐句总长的倒数

## Averaging X and T 对X与T进行平均处理

- Divide the time into intervals and ensure that the pitch X is the average within each interval.

- Since these musical pieces use the equal temperament system, let the reference frequency be f0=27.500. For any note a, with an interval of n semitones from the reference note, the frequency fa=f0·2^(X/1200).

- Convert all X in the sequence to frequencies and generate a new sequence file named average.txt.

- 将划分时间间隔，保证在每一个时刻内音高为X的平均数.

- 由于这些乐曲都是采用十二平均律，设基准音的频率为f0=27.500，任意一音a与基准音的音程为n个半音，则fa=f0·2^(X/1200).

- 将序列中所有X换算为频率产生新的序列文件average.txt.



