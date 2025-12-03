I just want to share a small network tools application that uses custom html inside Anvil with Pico CSS framework.

<img width="1077" height="899" alt="1" src="https://github.com/user-attachments/assets/2468bd7e-924c-49f7-ac90-59c3832a2f58" />

<img width="1077" height="899" alt="2" src="https://github.com/user-attachments/assets/884f9acb-7d3c-499a-8576-3fbb50cecb79" />


Although using custom html might be a bit outside of the scope i really liked Pico's approach of being a classless css framework. Meaning the plain html tags gets styled without writing any custom css. 

Eg just by adding the `<button>button</button>` html tag it gets styled by default.
![Screenshot 2025-12-03 at 13.39.51|256x172](upload://nctGmVmAqFW8sNipNoeoIFVEQ9l.png)

I have tried to keep the amount of custom CSS to a minimum. The CSS that is included is only there to ensure Pico CSS renders well inside an Anvil app :slight_smile: 

You can try out the app using the live link below.
Also, if you clone the app and want to change the color scheme you can just replace the cdn import in Native libraries with the cdn from the version picker link below.
```
<link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.pumpkin.min.css"
    >
```

Live link:
https://network-tools.anvil.app

Pico css:
https://picocss.com/

Pico css version picker:
https://picocss.com/docs/version-picker

Clone link:
https://anvil.works/build#clone:ROVU7EWAK6BMFYRB=MXGQTLBXMDXIVE3TW466NPUY
