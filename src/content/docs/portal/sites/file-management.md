---
title: File management actions
description: Copy, move and rename files, read a file's details, and make, list and unpack ZIP archives in the portal's folders, from forms, flows, endpoints and jobs.
---

File management actions copy, move and rename files in the portal's [folders](/portal/console/files/), read a file's details, and make, list and unpack ZIP archives. A form can file what was sent into the right folder, a job can pack a month's reports into one archive, and an endpoint can unpack an archive someone uploaded. They come with the portal's **Files** extension. As with every extension, they are open to every tenant of the portal.

They are [actions](/portal/sites/actions/) like any other: forms, flows, endpoints and jobs use them in their lists of actions. People can also move, rename and copy a file by hand under [Files](/portal/console/files/#move-or-copy-a-file) in the console.

## What people get

File management actions have no screen of their own. What they change is the files in a folder, and people open them where the folder lets them: anyone for a public folder, the people the folder names for a secure one (see [Files](/portal/console/files/#folders)).

## Copy, move and rename a file

Three actions change where a file is and what it is called:

- Copy a file writes a copy of a file, in the same folder or another.
- Move a file writes the copy, then removes the file it came from.
- Rename a file gives a file another name in its folder.

Each action names the file and its folder, and the names can be worked out as the action runs.

- A file keeps its extension: a PDF copied as `report.txt` fails with "A file keeps its extension: .pdf.".
- A file already there under the new name makes the action fail with "A file of that name is already there.", unless the action is set to replace it. Only someone who edits the folder may replace a file.
- Copying a file onto itself, or renaming it to the name it has, fails with "The file already has this name.".
- When a move has written the copy but cannot remove the file it came from, it fails and says so. Both files are then there; remove the old one by hand.

For now, this is set in the site's configuration: see [Developer: File management actions](/portal/developer/file-management/#copy-move-and-rename-a-file).

## Read a file's details

Reading a file's details gives its folder, its name, its size in bytes and the type it is served as, such as `application/pdf`. When there is no such file it gives nothing, so an action list can check whether a file is there before it makes one.

For now, this is set in the site's configuration: see [Developer: File management actions](/portal/developer/file-management/#read-a-files-details).

## ZIP archives

Three actions work with ZIP archives:

- Make an archive packs files into a `.zip`. It packs the files it names, or every file of the folder when it names none.
- List an archive's files lists the files in an archive.
- Unpack an archive writes each file of an archive into a folder.

An archive holds 1 to 100 files. Its name ends in `.zip`. Listing gives each file's name, as the archive holds it, with its folders, and its size. Unpacking gives the names it wrote, in the archive's order.

What an archive's files become when unpacked:
- Folders inside the archive are left out: each file takes the last part of its path.
- Names become what an upload's would: `Rapoarte/Raport Final (1).PDF` becomes `raport-final-1.pdf`.
- What a computer adds by itself, such as `__MACOSX`, `.DS_Store`, `Thumbs.db` and `desktop.ini`, is left out, and so are empty files.
- A file of a kind the portal does not keep, such as `setup.exe`, and two files that end up with the same name, make the whole archive fail, naming the file. Nothing is written.
- Unless the action is set to replace files, a file already there makes the whole archive fail too.

For now, this is set in the site's configuration: see [Developer: File management actions](/portal/developer/file-management/#zip-archives).

## Images

Resizing makes a resized copy of an image, such as a small preview of a photo someone uploaded:

- A width and a height: whole numbers from 1 to 4000; at least one of them.
- By default, the copy keeps the image's proportions within the width and height. It can instead fill them, cropping the middle, or fit the whole image and pad the rest, white for a JPEG, transparent otherwise.
- The new name's extension decides the format: `.jpg`, `.jpeg`, `.png`, `.webp` or `.avif`.
- A copy is never larger than the image itself, and it is turned the right way up. When the width and height make a box larger than the image, the box shrinks whole, keeping its shape.
- JPEG, PNG, WebP, AVIF and still GIF images are resized. An animated image, an image of more than 40 million pixels (16 million for AVIF), or any other file fails, saying why.

Reading an image's details gives its width, height and format, turned the right way up, or nothing when the file is not such an image or is not there.

For now, this is set in the site's configuration: see [Developer: File management actions](/portal/developer/file-management/#images).

## Files on a server

These actions exchange files with an FTP, FTPS or SFTP server, through a [file server connector](/portal/sites/connectors/#file-servers):

- Send files sends 1 to 20 files of a folder to the server, each under its own name.
- Fetch a file fetches one file into a folder.
- List a directory lists a directory of the server.
- Remove a file removes a file on the server.

The directory and the path on the server are under the connector's directory: names separated by `/`, never `.` or `..`. A path going above the directory fails before the server is reached.

- Sending refuses a name the server already has, before sending anything, unless the action is set to replace it. A file is sent under a temporary name and renamed when whole, so whoever reads the server never sees half a file.
- Listing gives each entry's name, size, whether it is a directory and when it was changed, at most 1,000 entries; the date is given when the server gives one plainly, else it is empty.
- Fetching an empty file fails: the portal keeps no empty file.
- Removing a file that is not there is no error.
- The server's own messages are never shown: a failure says what went wrong in the portal's words, such as "The server refused the username, password or key."

For now, this is set in the site's configuration: see [Developer: File management actions](/portal/developer/file-management/#files-on-a-server).

## Who may do what

File management actions keep to the folders' [permissions](/portal/sites/permissions/), as the file actions do. Someone who edits a folder reads its files, makes, replaces and removes them. Anyone else, a visitor too, only makes new files, and never in a public folder. So a form a visitor sends can copy a file into a secure folder, but cannot read, move or unpack one. Every folder is checked before any work is done.

An action that changes files changes the portal, so a GET or public [endpoint](/portal/sites/endpoints/) cannot use it. Reading a file's details, listing an archive's files and reading an image's details only read, and can be used anywhere. The actions on a server all reach another computer, so none of them is in a GET or public endpoint, listing a directory included.

On a server, the server's own account decides what the portal may do there; in the portal, a visitor's form can send a file to a server only from a folder the visitor may read, which is none, and fetch one only into a secure folder, as a new file.

## Limits

- A file is at most 10 MB, and the files one action reads at most 50 MB together.
- An archive unpacks to 100 files at most, each at most 10 MB, 50 MB in all, counted as they unpack, whatever the archive says of itself.
- Only plain ZIP archives are read: an encrypted archive, or a 64-bit one, fails with "The file is not a ZIP archive the portal can read.".
- A run changes 200 files at most, with these actions and the file actions together.
- A run takes 20 extension actions at most, these and the [document actions](/portal/sites/document-actions/) together.
- Unpacking into a folder the portal keeps itself writes every file at once, or none. Into a folder kept in a [bucket](/portal/console/files/#where-files-are-kept), files are written one after another; when the bucket stops answering part way, the action says how many were written.
- A run that is nearly out of time stops changing files. Pack or unpack many files in a [job](/portal/sites/jobs/), which has more time than a form.
- A file sent or fetched is at most 10 MB; one upload to a server sends 50 MB at most.
- A file server connector makes at most two calls at once; the others wait their turn, within the run's time.
- A flow's tests run no extension actions: a file management action fails the test.
