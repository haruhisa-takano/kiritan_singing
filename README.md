# kiritan_singing

(The original README in Japnese follows)

Labels for kiritan_singing data with extra resources for DNN-based singing voice synthesis (SVS) systems. The repository includes scripts to generate [sinsy](https://github.com/r9y9/sinsy)-compatible full-context labels, as well as semi-automatically corrected labels, which can be used to build DNN-based parametric SVS systems. Important features are summarized below:

- Full-context or mono label generation from musicxml files by [pysinsy](https://github.com/r9y9/pysinsy).
- DTW-based alignment between sinsy-generated labels and kiritan's alignment.
- Data preparation for training timelag/duration/acoustic models.
- Offset correction for songs 01 to 05. Ref [mmorise/kiritan_singing/issues/6](https://github.com/mmorise/kiritan_singing/issues/6)
- Audio file segmention based on simple heuristics.

I confirmed that pysinsy generates the same full-context labels with those produced by [NEUTRINO](https://n3utrino.work/). To know what the timelag/duration/acoustic models are, please have a look at some of SVS papers. e.g.,

- Y. Hono et al, "Recent Development of the DNN-based Singing Voice Synthesis System — Sinsy," Proc. of APSIPA, 2017.

See [DNN-SVS](https://github.com/r9y9/dnnsvs) to see how one can build SVS systems using the data provided in the repository.


## Requirements

- sinsy: https://github.com/r9y9/sinsy
- pysinsy: https://github.com/r9y9/pysinsy
- nnmnkwii (master): https://github.com/r9y9/nnmnkwii
- See also requirements.txt

## How to use

Due to the licensing issue, the repository does not include audio files. To generate data which is required for trainig SVS models using [DNN-SVS](https://github.com/r9y9/dnnsvs), please change `wav_dir` in `common.py` based on your environment. Then, please run:

```
run.sh
```

See comments in the `run.sh` for details. After running the script, you can findt the following there directories:

- `kiritan_singing_extra/timelag`
- `kiritan_singing_extra/duration`
- `kiritan_singing_extra/acoustic`

where labels and wav files used for building timelag/duration/acoustic models are stored. The directory structure is as follows:

### kiritan_singing_extra/timelag

```
tree kiritan_singing_extra/timelag/ -L 1
kiritan_singing_extra/timelag/
├── label_phone_align
└── label_phone_score
```

### kiritan_singing_extra/duration

```
tree kiritan_singing_extra/duration/ -L 1
kiritan_singing_extra/duration/
└── label_phone_align
```

### kiritan_singing_extra/acoustic

```
tree kiritan_singing_extra/acoustic -L 1
kiritan_singing_extra/acoustic
├── label_phone_align
└── wav
```

## Acknowledgements

I would like to thank Prof. Morise and authors of the kiritan_singing database for thier continuous improvements and kind support.

Ryuichi Yamamoto

# 東北きりたん歌唱データベースのラベルデータ
東北きりたん歌唱データベース（きりたん歌唱DB）の最新ラベルデータを共有するためのリポジトリです．データベースの本体は[こちら](https://zunko.jp/kiridev/login.php)からダウンロードできます．midi_label，mono_labelに加えてMusicXMLも公開しました．

## 本リポジトリで配布するデータとGitHubで公開する動機
本データベースのラベルにはmidi_labelとmono_labelとがあり，それぞれ譜面データと音素境界のデータとなります．MIDIについてはMelodyneで自動採譜した後に手動で調整したものを配布していますが，楽曲によっては採譜そのものが困難な場合や，キーが曖昧でずれてしまっている場合があります．これら以外にも，実際に利用してみて判明する問題もあると考えられることから，ご利用者の皆様の修正案をここで議論できればと思い，ラベルデータのみGitHubで管理することにしました．

ラベルデータは本リポジトリで修正できますが，歌唱ファイルを修正する前処理はここで処理できません．修正のアイディアをissueで投げて頂ければ，本readmeに反映するように致します．明確なミスの場合はすぐ差し換えますが，微妙な差についてはissue内で差し換え・掲載するべきか議論する形にさせてください．以下の例のように情報は逐次更新していき，修正にご協力頂いた皆様のお名前はできるだけクレジットさせて頂く予定です．なお，本データベースはあくまでも改正著作権法30条の4に定められた範囲での利用に限定されていますので，本リポジトリやそれ以外の場所においても範囲を逸脱した使途にならないようにお気をつけください．

## 現時点で判明しているラベルの問題点
- 08: 前半部分の採譜が極めて困難なため，MIDIそのものが存在しない

## その他データベースについて品質を上げるための工夫
- 08: 歌声そのものについて，推定されたF0がMIDIとずれているため学習前にF0をMIDIに寄せたほうが良い

## 修正履歴
- 2020/01/06: 44の276行目/m/が抜けていたので追加
- 2020/01/06: 39の143行目/u/が抜けていたので追加
- 2020/01/06: 38の217行目/i/が抜けていたので追加
- 2020/01/06: 20の326, 334行目/t/->/ts/
- 2020/01/06: 16の390行目/a/が抜けていたので追加
- 2020/01/06: 15の318行目/sh/->/s/
- 2019/11/25: 06の後半部分のMIDIラベルが無かったので追加
- 2019/11/22: MIDIラベルの13と14が逆だったので入れ替え

## ご協力頂いた皆様
@Auxilyrica 様，Hiroshiba 様，dhgrs 様，匿名希望様，ご協力ありがとうございます．
