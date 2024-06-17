
# kernel-fsync

![](https://copr.fedorainfracloud.org/coprs/sentry/kernel-fsync/package/kernel/status_image/last_build.png)

Fork of the Fedora [kernel package](https://src.fedoraproject.org/rpms/kernel) to add fixes and new features.


### I have a patch I want you to include

Feel free to open an issue about it and I'll look into it to see if its worth while including.
Do note that :
- it must not negatively affect users more than they already are
- if it can be packaged externally, it will likely not be included
- it must be available under an open source license
- system stability and security must not be impacted in major ways


### Whats the deal with the name?

kernel-fsync started out as a fork of the Fedora kernel with the fsync patchset for wine included.
The patches were lated rebranded as futex2 because of confusion, but  the name was kept for the kernel.

The name may be changed in the future.

### How to build
To build the kernel you need to manual the relevant kernel tarball from somewhere and put it into the `SOURCES` directory.

From then out you can use the script located at `TOOLS/build.sh` to run the `rpmbuild` with some predefined values.

Building the kernel as it can then be done like this:
`./TOOLS/build.sh -ba SPECS/kernel.spec`

### Friends of Fsync
- [Fedora](https://fedoraproject.org)
- [Nobara Project](https://nobaraproject.org/)
- [Bazzite](https://bazzite.gg/)
- [CachyOS](https://cachyos.org/)
- [Frogging Family](https://github.com/Frogging-Family)
