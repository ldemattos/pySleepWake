# pySleepWake

pySleepWake is a set of two small Python scripts that manages the process of suspending and waking up computers.

The script sleep.py is the one in charge of suspending the computer based on the average network traffic in a given time window. On the other hand, the script alarm.py is the one responsible for waking up the suspended computer through network when some other device is looking for it.

In conf/ directory there are cofiguration file samples for both alarm.py and sleep.py.

In systemd/ directory there are configurations samples for GNU/Linux systemd startup unit files.

All the scripts must be executed as root, since they perform administrative tasks such as suspending and executing etherwake.

The log files are by default stored in /var/log, however this behavior can be changed in the configurations files.

This project was developed with a domestic NAS (Network Attached Storage) in mind, since its usage rate do not requires a computer operating 24h/7, neither the power dispensed, the heat and/or the noise. A on demand approach seems a much better in that case.

Both scripts were designed and tested in GNU/Linux. I suppose that with minimum effort it should be portable through all Unix-flavors.

## Contribution

Is welcome and wanted!

## Licensing

[GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.en.html)
