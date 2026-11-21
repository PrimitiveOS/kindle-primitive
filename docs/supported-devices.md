# Jailbreakable Kindles: the supported-devices list

Status date: 2026-11-21. Written for: the launcher's "select your Kindle" model table (`kl-core/src/models.rs`, the list the owner picks from) and anyone
adding a model. Decision D3 of [device-profile-plan.md](device-profile-plan.md).

## How to read the table

- **Firmware** is the range the jailbreak works on today, from the SpiderCat project (the widest current exploit).
- **Arch** is `armhf` (hard-float): SpiderCat's README says its builds are hard-float. Every model here is listed as
  armhf until its own build is checked on the device. Our install gate is the arch, so this column must be right.
- **Verified** says whether we have run PrimitiveOS on that model. Only the Oasis 3 is.
- Older models (Kindle 7–8, Paperwhite 1–3, Voyage, Oasis 1–2) only have exploits for firmware below 5.16.3, so they
  are not listed: no current firmware can be jailbroken on them with the tools we know.

| Model | Codename(s) | Firmware (SpiderCat) | Arch | Verified | Source |
|---|---|---|---|---|---|
| Kindle Oasis 3 | KO3, KOA3; platform `zelda` | 5.16.3–5.19.5 | armhf | **yes** (5.18.2, device probe) | [SpiderCat](https://github.com/KindleModding/SpiderCat), [BookFere table](https://en.bookfere.com/post/jailbreak-compatibility-check.html) |
| Kindle Paperwhite 5 | PW5, KPW5 | 5.16.3–5.19.5 | armhf (expected) | no | BookFere table |
| Kindle Paperwhite 5 Signature Edition | KPW5SE | 5.16.3–5.19.5 | armhf (expected) | no | BookFere table |
| Kindle Paperwhite 6 | PW6 | 5.16.3–5.19.5 | armhf (expected) | no | BookFere table |
| Kindle Paperwhite 4 | PW4, KPW4 | 5.16.3–5.19.5 | armhf (expected) | no | BookFere table |
| Kindle 11 (2022) | KT5, K11 | 5.16.3–5.19.5 | armhf (expected) | no | BookFere table |
| Kindle 11 (2024) | KT6 | 5.16.3–5.19.5 | armhf (expected) | no | BookFere table |
| Kindle 10 (2019, Basic) | KT4, K10 | 5.16.3–5.19.5 | armhf (expected) | no | BookFere table |
| Kindle Colorsoft | KC | 5.16.3–5.19.5 | armhf (expected) | no | BookFere table |
| Kindle Scribe (2022) | KS1 | 5.16.3–5.19.5 | armhf (expected) | no | BookFere table |
| Kindle Scribe (2024) | KS2 | 5.16.3–5.19.5 | armhf (expected) | no | BookFere table |

## What is not settled

- **Arch per model.** "armhf (expected)" means the model is in the hard-float SpiderCat list, not that we checked its
  loader on the device. Check `/lib/ld-linux-armhf.so.3` and `uname -m` on each model before it is marked verified.
- **Firmware floor.** The sources conflict on 5.16.3 for some exploits. The launcher does not gate on firmware (owner
  decision), so this only changes what the jailbreak page says.
- **Scribe 3 and Scribe Colorsoft** are listed by BookFere as "support pending". They are not in the list.
- **The BookFere table is a third-party compilation.** Verify each row against its exploit's own page before a model is
  added to the launcher's list.
