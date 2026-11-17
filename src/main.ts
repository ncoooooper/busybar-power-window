import {surface,panel,label,rect,mint,amber,report,type Frame} from "@shared/surface";
import {loadValues} from "@shared/settings";

type Snapshot={charge:number;state:string;source:string;window:null|{active:boolean;minutes:number}};
let sample:Snapshot|null=null, url="", message="Loading settings", page=0, busy=false,closed=false,lastTry=0;
let timer:ReturnType<typeof setInterval>|undefined;
function draw():Frame{
 const title=!sample?(url?"Check bridge":"Power setup"):page===0?sample.charge+"%  "+sample.source:sample.window?(sample.window.active?"Restore":"Outage")+" "+sample.window.minutes+"m":"No window";
 const trend=sample?.window?(sample.window.active?"Window ends in ":"Outage in ")+sample.window.minutes+" min":"No upcoming window";
 const filled=Math.round((sample?.charge||0)*72/100);
 return [label("value",title,0,0,page===0?mint:amber),
 ...(filled>0?[rect("charge",0,12,filled,3,mint)]:[]),
 ...(filled<72?[rect("track",filled,12,72-filled,3,"#29373FFF")]:[]),
 ...panel("POWER WINDOW",[message,sample?"Reserve "+sample.charge+"% / "+sample.state:"Set bridge URL in settings",sample?trend:"Run bridge/power.py",
 "Wheel: switch view","Click: refresh","Automatic refresh: 60 sec"])];
}
async function poll(){
 if(!url||busy||closed||Date.now()-lastTry<1500)return;
 busy=true;lastTry=Date.now();
 try{
   const response=await fetch(url);if(!response.ok)throw Error("HTTP "+response.status);
   const value=await response.json() as Snapshot;
   if(typeof value.charge!=="number"||value.charge<0||value.charge>100||typeof value.source!=="string"||!["mains","battery","unknown"].includes(value.state)||
     (value.window!==null&&(!value.window||typeof value.window.active!=="boolean"||!Number.isFinite(value.window.minutes))))throw Error("Invalid reading");
   sample=value;message="Live from "+value.source;console.log("power",sample.charge,sample.state,sample.window?.minutes);
 }catch(error){message=sample?"Offline / last reading":"Bridge offline";console.log("power offline",String(error));}
 finally{busy=false;if(!closed)refresh();}
}
const refresh=surface(draw,k=>{if(k==="ok"||k==="start")void poll();if(k==="up"||k==="down")page=1-page;},()=>{closed=true;if(timer!==undefined)clearInterval(timer);});
void loadValues().then(v=>{
 if(closed)return;url=String(v?.bridge||"").trim();message=url?"Connecting":"Setup required";refresh();
 if(url){void poll();timer=setInterval(()=>void poll(),60000);}
}).catch(report);
