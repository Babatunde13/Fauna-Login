// var hostile = require('hostile')

// var domains = [
//   {
//     ip: '127.0.0.1', 'domain': 'peercdn.com'
//   },
//   {
//     ip: '127.9.0.2', 'domain': 'babatunde.com'
//   },
//   {
//     'ip': '0.0.0.0', 'server': 'aby.eldonapp.com'
//   },
//   {
//     'ip': '0.0.0.0', 'server': 'test.eldonapp.com'
//   },
//   {
//     'ip': '0.0.0.0', 'server': 'handbook.eldonapp.com'
//   },
//   {
//     'ip': '0.0.0.0', 'server': 'corpjobs.eldonapp.com'
//   },
//   {
//     'ip': '0.0.0.0', 'server': 'urlrewriter.eldonapp.com'
//   },
//   {
//     'ip': '0.0.0.0', 'server': 'assistant.eldonapp.com'
//   },
//   {
//     'ip': '0.0.0.0', 'server': 'charts.eldonapp.com'
//   },
//   {
//     'ip': '0.0.0.0', 'server': 'hio.eldonapp.com'
//   },
//   {
//     'ip': '0.0.0.0', 'server': 'docs.eldonapp.com'
//   },
//   {
//     'ip': '0.0.0.0', 'server': 'eldonlabs.eldonapp.com'
//   },
//   {
//     'ip': '0.0.0.0', 'server': 'playground.eldonapp.com'
//   },
//   {
//     'ip': '0.0.0.0', 'server': 'eldontemplate.eldonapp.com'
//   },
//   {
//     'ip': '0.0.0.0', 'server': 'eldonworkflow.eldonapp.com'
//   },
//   {
//     'ip': '0.0.0.0', 'server': 'mongodblocal.eldonapp.com'
//   }
// ]

// // domains.forEach(ele => {
// //   hostile.set(ele['ip'], ele['server'], function (err) {
// //     if (err) {
// //       console.error(err)
// //     } else {
// //       console.log(`set /etc/hosts successfully for $ele['server']!`)
// //     }
// //   })
  
// // })

// var preserveFormatting = false
 
// hostile.get(preserveFormatting, function (err, lines) {
//   if (err) {
//     console.error(err.message)
//   }
//   console.log(lines)
//   lines.forEach(function (line) {
//     console.log(line) // [IP, Host]
//   })
// })


var Hosts = require('hosts-so-easy');
const hosts = Hosts.Hosts();

// hosts file is written once at the end
hosts.add('192.168.0.1', 'www');
hosts.add('192.168.1.1', [ 'mongo', 'db' ]);

// this is completely safe, only one write occurs at the end.
for (let i = 2; i < 10; i++)
  hosts.add('192.168.0.'+i, 'host'+i);