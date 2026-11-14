---
title: File management actions
description: Copy, move and rename files, read a file's details, and make, list and unpack ZIP archives in the portal's folders, from forms, flows, endpoints and jobs.
---

File management actions copy, move and rename files in the portal's [folders](/portal/console/files/), read a file's details, and make, list and unpack ZIP archives. A form can file what was sent into the right folder, a job can pack a month's reports into one archive, and an endpoint can unpack an archive someone uploaded. They come with the portal's **Files** extension. As with every extension, they are open to every tenant of the portal.

They are [actions](/portal/sites/actions/) like any other: put them in a form's, a flow's, an endpoint's or a job's action list. People can also move, rename and copy a file by hand under [Files](/portal/console/files/#move-or-copy-a-file) in the console.

## What people get

File management actions have no screen of their own. What they change is the files in a folder, and people open them where the folder lets them: anyone for a public folder, the people the folder names for a secure one (see [Files](/portal/console/files/#folders)). Each action below has its example in the [config example](#config-example).

## Copy, move and rename a file

| Type | What it does | Takes |
|---|---|---|
| `copyFile` | Writes a copy of a file, in the same folder or another | `folder`, `name`, `toFolder`, `toName`, `replace` |
| `moveFile` | Writes the copy, then removes the file it came from | `folder`, `name`, `toFolder`, `toName`, `replace` |
| `renameFile` | Gives a file another name in its folder | `folder`, `name`, `toName`, `replace` |

- `name` and `toName` are expressions; `folder` and `toFolder` name folders.
- A file keeps its extension: a PDF copied as `report.txt` fails with "A file keeps its extension: .pdf.".
- A file already there under `toName` makes the action fail with "A file of that name is already there.", unless `replace: true`. Only someone who edits the folder may replace a file.
- Copying a file onto itself, or renaming it to the name it has, fails with "The file already has this name.".
- When a move has written the copy but cannot remove the file it came from, it fails and says so. Both files are then there; remove the old one by hand.

## Read a file's details

`fileInfo` keeps a file's details in `vars.<into>` as `{ folder, name, size, type }`: its size in bytes and the type it is served as, such as `application/pdf`. When there is no such file it keeps `null`, so an action list can check whether a file is there before it makes one (see the [config example](#the-details-of-a-file)).

## ZIP archives

| Type | What it does | Takes |
|---|---|---|
| `zipFiles` | Packs files into a `.zip` | `folder`, `names` (a list; every file of the folder when left out), `toFolder`, `toName`, `replace` |
| `zipNames` | Lists the files in an archive | `folder`, `name`, `into` |
| `unzipFile` | Writes each file of an archive into a folder | `folder`, `name`, `toFolder`, `into` (optional), `replace` |

- An archive holds 1 to 100 files. Its name ends in `.zip`.
- `zipNames` keeps a list of `{ name, size }`, each name as the archive holds it, with its folders.
- `unzipFile` keeps the names it wrote in `vars.<into>`, in the archive's order.

What an archive's files become when unpacked:
- Folders inside the archive are left out: each file takes the last part of its path.
- Names become what an upload's would: `Rapoarte/Raport Final (1).PDF` becomes `raport-final-1.pdf`.
- What a computer adds by itself, such as `__MACOSX`, `.DS_Store`, `Thumbs.db` and `desktop.ini`, is left out, and so are empty files.
- A file of a kind the portal does not keep, such as `setup.exe`, and two files that end up with the same name, make the whole archive fail, naming the file. Nothing is written.
- Without `replace: true`, a file already there makes the whole archive fail too.

## Files on a server

These actions exchange files with an FTP, FTPS or SFTP server, through a [file server connector](/portal/sites/connectors/#file-servers):

| Type | What it does | Takes |
|---|---|---|
| `ftpUpload` | Sends 1 to 20 files of a folder to the server, each under its own name | `connector`, `folder`, `names` (a list), `remoteDir`, `replace` |
| `ftpDownload` | Fetches one file into a folder | `connector`, `remotePath`, `toFolder`, `toName`, `replace` |
| `ftpList` | Lists a directory of the server | `connector`, `remoteDir`, `into` |
| `ftpDelete` | Removes a file on the server | `connector`, `remotePath` |

- `remoteDir` and `remotePath` are expressions, under the connector's directory: names separated by `/`, never `.` or `..`. A path going above the directory fails before the server is reached.
- `ftpUpload` refuses a name the server already has, before sending anything, unless `replace: true`. A file is sent under a temporary name and renamed when whole, so whoever reads the server never sees half a file.
- `ftpList` keeps a list of `{ name, size, directory, modified }`, at most 1,000 entries; `modified` is a date when the server gives one plainly, else `null`.
- `ftpDownload` of an empty file fails: the portal keeps no empty file.
- `ftpDelete` of a file that is not there is no error.
- The server's own messages are never shown: a failure says what went wrong in the portal's words, such as "The server refused the username, password or key."

## Who may do what

File management actions keep to the folders' [permissions](/portal/sites/permissions/), as the file actions do. Someone who edits a folder reads its files, makes, replaces and removes them. Anyone else, a visitor too, only makes new files, and never in a public folder. So a form a visitor sends can copy a file into a secure folder, but cannot read, move or unpack one. Every folder is checked before any work is done.

An action that changes files changes the portal, so a GET or public [endpoint](/portal/sites/endpoints/) cannot use it. `fileInfo` and `zipNames` only read, and can be used anywhere. The actions on a server all reach another computer, so none of them is in a GET or public endpoint, `ftpList` included.

On a server, the server's own account decides what the portal may do there; in the portal, a visitor's form can send a file to a server only from a folder the visitor may read, which is none, and fetch one only into a secure folder, as a new file.

## Limits

- A file is at most 10 MB, and the files one action reads at most 50 MB together.
- An archive unpacks to 100 files at most, each at most 10 MB, 50 MB in all, counted as they unpack, whatever the archive says of itself.
- Only plain ZIP archives are read: an encrypted archive, or a 64-bit one, fails with "The file is not a ZIP archive the portal can read.".
- A run changes 200 files at most, with these actions and the file actions together.
- A run takes 20 extension actions at most, these and the [document actions](/portal/sites/document-actions/) together.
- Unpacking into a folder the portal keeps itself writes every file at once, or none. Into a folder kept in a [bucket](/portal/console/files/#where-files-are-kept), files are written one after another; when the bucket stops answering part way, the action says how many were written.
- A run that is nearly out of time stops changing files. Pack or unpack many files in a [job](/portal/sites/jobs/), which has more time than a form.
- A file sent or fetched is at most 10 MB; one `ftpUpload` sends 50 MB at most.
- A file server connector makes at most two calls at once; the others wait their turn, within the run's time.
- A flow's tests run no extension actions: a file management action fails the test.

## Config example

These go in an action list: a form's `actions` (`forms/<id>.yaml`), a flow, an endpoint or a job.

### A file moved where it belongs

```yaml
- type: moveFile
  folder: inbox
  name: '"cerere-" + submission.id + ".pdf"'
  toFolder: approved
  toName: '"cerere-" + submission.id + ".pdf"'
```

- `folder` and `name`: the file to move.
- `toFolder` and `toName`: where it goes, and its name there.

A file renamed in its folder, replacing one of that name:

```yaml
- type: renameFile
  folder: reports
  name: '"draft.pdf"'
  toName: '"final.pdf"'
  replace: true
```

- `replace: true`: a file already named `final.pdf` is replaced.

### The details of a file

```yaml
- type: fileInfo
  folder: reports
  name: '"raport-" + vars.month + ".pdf"'
  into: report
- type: copyFile
  condition: vars.report != null
  folder: reports
  name: vars.report.name
  toFolder: archive
  toName: vars.report.name
```

- `into`: where the details are kept, or `null` when there is no such file.
- The copy is made only when the report is there.

### Files sent to a server and fetched from it

```yaml
- type: ftpUpload
  connector: registry
  folder: approved
  names: '["cerere-" + submission.id + ".pdf"]'
  remoteDir: '"incoming"'
- type: ftpDownload
  connector: registry
  remotePath: '"answers/raspuns-" + submission.id + ".pdf"'
  toFolder: answers
  toName: '"raspuns-" + submission.id + ".pdf"'
```

- `connector`: a file server connector.
- `names`: the files of `folder` to send.
- `remoteDir`: where they go, under the connector's directory.
- `remotePath`: the file to fetch, and `toFolder` and `toName`: where it is kept.

### An archive packed and unpacked

```yaml
- type: zipFiles
  folder: reports
  toFolder: archive
  toName: '"rapoarte-" + vars.month + ".zip"'
```

- `names` is left out, so every file of `reports` is packed.
- `toFolder` and `toName`: where the archive is kept.

```yaml
- type: unzipFile
  folder: uploads
  name: '"documente.zip"'
  toFolder: received
  into: received
```

- `folder` and `name`: the archive.
- `toFolder`: where its files are written.
- `into`: the names written, in the archive's order.
