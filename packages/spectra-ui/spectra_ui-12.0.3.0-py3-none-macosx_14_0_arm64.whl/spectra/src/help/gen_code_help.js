"use strict";

function leastSquareN(points, dim) {
	if(points.length < dim) {
		return numeric.rep([dim], 0);
	}
	var A = numeric.rep([dim, dim], 0);
	var b = numeric.rep([dim], 0);
	for(var i = 0; i < points.length; i++) {
		for(var j = 0; j < dim; j++) {
			for(var k = 0; k < dim; k++) {
				A[j][k] += Math.pow(points[i][0], 2*(dim-1)-j-k);
			}
		}
		for(var j = 0; j < dim; j++) {
			b[j] += points[i][1]*Math.pow(points[i][0], dim-1-j);;
		}
	}
	var c = numeric.solve(A, b)
	return c;
}

//-------------------------
// create field distribution file for SC3
//-------------------------

function RadLength(Nper, lu, symm)
{
    let L = lu*(symm?1.5:2.0);
    if(Nper > 1){
        L += lu*(Nper-1);
    }
    return L;
}

function GenerateMPField(Nper, lu, K, zini, dzbase, symm, z, bx, by, pfactor, simple = false)
{
    let Bp = K/lu/COEF_K_VALUE;
    let ku = 2.0*Math.PI/lu;
    let L = RadLength(Nper, lu, symm);
    let pointspp = Math.floor(0.5+L/dzbase);
    let dz = L/pointspp;
    let isendfactor = Array.isArray(pfactor);

    let zorg = zini+L/2.0, jsec;
    let bdr, phase, bcoef, zr;
    phase = symm ? 0 : -Math.PI/2.0;
    if(simple){ // -1/2, 1, 1/2
        bdr = [lu/4.0];
        bcoef = [0.5];
    }
    else if(symm && Nper == 1){ // -1/2, 1, 1/2
        bdr = [lu/4.0];
        bcoef = [0.5];
    }
    else{        
        if(Nper > 1){ // -1/4, -3/4, 1,...., 3/4, 1/4
            bdr = [lu/2.0, 0];
            bcoef = [1.0/4.0, 3.0/4.0];
        }
        else{
            bdr = [lu/2.0];
            bcoef = [1.0/3.0];    
        }
    }
    if(Nper > 1){
        for(jsec = 0; jsec < bdr.length; jsec++){
            if(simple){
                bdr[jsec] += (Nper-1)*lu*0.5;
            }
            else if(symm){
                bdr[jsec] += (Nper-1.5)*lu*0.5;
            }
            else{
                bdr[jsec] += (Nper-1)*lu*0.5;
            }
        }
    }
    for(let n = 0; n < pointspp; n++){
        zr = n*dz+zini;
        z.push(zr);
        let br = Bp*Math.cos(ku*(zr-zorg)+phase);
        for(jsec = 0; jsec < bdr.length; jsec++){
            if(Math.abs(zr-zorg) >= bdr[jsec]){
                break;
            }    
        }
        if(jsec < bdr.length){
            if(isendfactor){
                if(zr < zorg){
                    br *= pfactor[0];
                }
                else{
                    br *= pfactor[1];
                }
            }
            else{
                br *= bcoef[jsec];
            }
        }
        by.push(br);
        bx.push(0.0);
    }
    return zr+dz;
}

function GenerateHelicalRetarder(L, K, zini, dzbase, z, bxy)
{
    let lu = L*0.5;
    let ku = 2.0*Math.PI/lu;
    let pointspp = Math.ceil(L/dzbase);
    let dz = L/pointspp;

    let zorg = zini+L/2.0, zr, jsec;

    let phase = [0, -Math.PI/2.0];
    let bdo = [3.0*lu/4.0, lu];
    let bdr = [lu/4.0, lu/2.0];
    let bcoef = [0.5, 1.0/3.0];
    let Bp = K/lu/COEF_K_VALUE;
    for(let n = 0; n < pointspp; n++){
        zr = n*dz+zini;
        z.push(zr);
        for(let j = 0; j < 2; j++){
            let br = Bp*Math.cos(ku*(zr-zorg)+phase[j]);
            if(Math.abs(zr-zorg) >= bdo[j]){
                br = 0;
            }
            else if(Math.abs(zr-zorg) >= bdr[j]){
                br *= bcoef[j];
            }
            bxy[j].push(br);
        }
    }
    return zr+dz;
}

function Smoothing(havgp, tarr, jarr, jnew)
{
    let points = [];
    for(let n = 0; n < tarr.length; n++){
        for(let m = -havgp; m <= havgp; m++){
            let mi = m+n;
            if(mi >= 0 && mi < tarr.length){
                points.push([tarr[mi], jarr[mi]]);
            }
        }
        let a = leastSquareN(points, 4);
        jnew.push(
            ((a[0]*tarr[n]+a[1])*tarr[n]+a[2])*tarr[n]+a[3]
        );
        points.length = 0;
    }
}

function GetPeakPositionsFit(havgp, tarr, jarr, tpeak, jpeak, threshold, skiptr)
{
    let points = [];
    let ncurr = 0;
    for(let n = 1; n < tarr.length-1; n++){
        points.length = 0;
        for(let m = -havgp; m <= havgp; m++){
            let mi = m+n;
            if(mi >= 0 && mi < tarr.length){
                points.push([tarr[mi], jarr[mi]]);
            }
        }
        let a = leastSquareN(points, 3);
        if(a[0] >= 0){
            continue;
        }
        let pkpos = -a[1]/2/a[0];
        let peak = a[2]-a[1]**2/4/a[0];
        peak = GetParabolic(tarr, jarr, pkpos);
        if((pkpos-tarr[n-1])*(pkpos-tarr[n+1]) < 0 
                && peak > threshold && Math.abs(pkpos) > skiptr){
            if(n > ncurr+havgp){
                tpeak.push(pkpos);
                jpeak.push(peak);
                ncurr = n;   
            }
        }
    }
}

function GetEndFactor(lamhat, Lint, lu, K, pol)
{
    let Lhat = Lint/lu;
    let D = ((lamhat-Lhat)/K**2-5.0/8.0)/(4*Lhat-4.5);
    if(D < 0){
        return null;
    }
    let alpha = pol*Math.sqrt(D);

    let lamhatr = Lhat+K**2*(5.0/8.0+alpha**2*(4*Lhat-4.5));

    alpha += 0.5;
    let theta = K/(1500/0.511)*(1-2*alpha);

    return alpha;
}


function GetPoleFactor(lamhat, Lint, lu, K, pol)
{
    let Lhat = Lint/lu;
    let D = ((lamhat-Lhat)/K**2-5.0/8.0)/(Lhat-0.25);
    if(D < 0){
        return null;
    }
    let alpha = pol*Math.sqrt(D);

    let lamhatr = Lhat+K**2*(5.0/8.0+alpha**2*(Lhat-0.25));

    return alpha;
}

function GenerateField4SC3(flip, epret, 
    isempt = false, dbl = false, thresh = 1.5, norsl = 1, norpos = -1, Lchc = 0.3, skiptr = 0)
{
    let eloss = 0;
//    eloss=parseFloat(window.prompt("Input average energy loss/section", "0"));

    let gam2 = 1.0/(GetObj(AccLabel)[AccPrmsLabel.gaminv]*0.001);
    gam2 *= gam2;
    let srcobj = GetObj(SrcLabel);
    let segobj = srcobj[SrcPrmsLabel.segprm[0]];
    let symm = srcobj[SrcPrmsLabel.field_str[0]] == SymmLabel;
    let lu = srcobj[SrcPrmsLabel.lu]*0.001; // mm -> m
    let Nrad = srcobj[SrcPrmsLabel.periods];
    let dzbase = lu/100;
    let K = srcobj[SrcPrmsLabel.Kperp];
    let Lrad = RadLength(Nrad, lu, symm);
    let Lret;
    let td;
    if(dbl){
        td = norsl;
    }

    let bunchtype = GetObj(AccLabel)[AccOptionsLabel.bunchtype[0]];
    let tarr = [], jarr = [], ttmp, jtmp;
    if(bunchtype == CurrProfLabel){
        let obj = GetObj(AccLabel)[AccOptionsLabel.currdata[0]];
        ttmp = CopyJSON(obj.data[0]);
        jtmp = CopyJSON(obj.data[1]);
    }
    else if(bunchtype == EtProfLabel){
        let obj = GetObj(AccLabel)[AccOptionsLabel.Etdata[0]];
        ttmp = CopyJSON(obj.data[0]);
        let earr = CopyJSON(obj.data[1]);
        etarr = CopyJSON(obj.data[2]);
        for(let n = 0; n < ttmp.length; n++){
            let jc = 0;
            for(let m = 0; m < earr.length; m++){
                jc += etarr[m*ttmp.length+n]
            }
            jtmp.push(jc);
        }
    }
    else{
        Alert("Bunch profile not valid.");
        return;
    }   

    let havgpoints = 3;
    let jnew = [];
    Smoothing(havgpoints, ttmp, jtmp, jnew);
    let plotid = AttachSuffix(GetIDFromItem(AccLabel, AccOptionsLabel.currdata[0], -1), SuffixPlotBody);

    let plobj = document.getElementById(plotid);
    let nplots = plobj.data.length;
    for(let i = 1; i < nplots; i++){
        Plotly.deleteTraces(plotid, 1);
    }

    Plotly.addTraces(plotid, {x:ttmp, y:jnew, name:"Fit Result"});  

    let tpeak = []; 
    let jpeak = [];
    let javg = jtmp.reduce((acc, curr)=>acc+curr)/jtmp.length;
    GetPeakPositionsFit(havgpoints, ttmp, jnew, tpeak, jpeak, javg*thresh, skiptr)
    if(tpeak.length < 2){
        Alert("Number of current peaks is less than 2.");
        return;
    }

    let M = segobj[SegPrmsLabel.segments];
    let iniM = 0;
    if(M < tpeak.length){
        iniM = Math.floor((tpeak.length-M)/2);
        let incr = jpeak[iniM] > jpeak[iniM+M] ? -1 : 1;
        while((incr < 0 && jpeak[iniM] > jpeak[iniM+M]) 
            || (incr > 0 && jpeak[iniM] < jpeak[iniM+M])){
            iniM += incr;
        }
        if(jpeak[iniM] < jpeak[iniM+M+1]){
            iniM++;
        }
    }
    else{
        M = tpeak.length-1;
    }

    let tpick = tpeak.slice(iniM, M+iniM+1);
    let jpick = jpeak.slice(iniM, M+iniM+1);

    if(eloss != 0){
        for(let m = 1; m <= M; m++){
            tpick[M-m] += (tpick[M]-tpick[M-m])*eloss*m*2;
        }
    }

    if(!dbl){
        Plotly.addTraces(plotid, {x:tpick, y:jpick, name:"Peak Positions", mode:"markers",
        marker:{symbol:"circle-open", size:15, color:"black"}});
    }

    if(norpos >= 0){
        let jp = M-norpos;
        if(jp < 1 || jp > tpick.length){
            Alert("Position to tune the slippaeg is out ouf range");
            return;
        }
        let slpos = [[tpick[jp], tpick[jp-1]], [jpick[jp], jpick[jp-1]]];
        Plotly.addTraces(plotid, {x:slpos[0], y:slpos[1], name:"Slippage Tuned", mode:"lines", 
            line:{color:"green"}});
    }        

    let pdelay = segobj[SegPrmsLabel.phi0]/2.0;
    if(pdelay > 1){ // double pulse option
        Lret = segobj[SegPrmsLabel.interval]/2-Lrad;
    }
    else{
        Lret = segobj[SegPrmsLabel.interval]-Lrad;
        pdelay = 0;
    }
    let luret = epret ? Lret/2.0 : Lret/1.5;
    let luretch = Lchc/1.5;
    let Kpret = 0;
    if(pdelay > 1){
        pdelay *= srcobj[SrcPrmsLabel.lambda1]*1e-9;
        Kpret = (pdelay*16*gam2/luret-12)/5;
        if(Kpret < 0){
            Alert("Interval of the double pulse too short.");
            return;    
        }
        Kpret = Math.sqrt(Kpret);
    }

    let z = [], bx = [], by = [], secno = [], raddelay, radpermin, radKmin = 2;

    if(symm && Nrad == 1){
        raddelay = lu*(12+5*K*K)/16/gam2;
    }
    else{
        raddelay = lu/gam2;
        if(Nrad > 1){
            raddelay += lu*7*K*K/32/gam2;
        }
        else{
            raddelay += lu*7*K*K/18/gam2;
        }
    }
    radpermin = lu*(1+radKmin**2/2)/2/gam2/CC*1e15;
    if(Nrad > 1){
        if(symm){
            raddelay += (Nrad-1.5)*lu*(1+K*K/2)/2/gam2;
        }
        else{
            raddelay += (Nrad-1)*lu*(1+K*K/2)/2/gam2;
        }
    }
    if(Kpret > 0){
        raddelay *= 2;
    }

    if(dbl){
        let tmin = (raddelay+pdelay+Lret/2/gam2)/CC*1e15;
        td = Math.abs(td);
        let tpeak2 = Array.from(tpeak, t => t+td);
        let index = [0, tpeak.length-1];
        while(tpeak[index[0]] < tpeak2[0]){
            index[0]++;            
        }
        while(tpeak2[index[1]] > tpeak[tpeak.length-1]){
            index[1]--;            
        }
        let tnew = [tpeak2[0]];
        let jnew = [jpeak[0]];
        let curr = 0;
        let currindex = [index[0], 0]
        let ts = [tpeak, tpeak2];
        do{
            let dt;
            while((dt = ts[curr][currindex[curr]]-tnew[tnew.length-1]) < tmin){
                currindex[curr]++;
                if(currindex[curr] >= tpeak.length){
                    break;
                }
            }
            tnew.push(ts[curr][currindex[curr]]);
            jnew.push(jpeak[currindex[curr]]);
            curr = 1-curr;
            currindex[curr]++;
        } while(currindex[0] < tpeak.length || currindex[1] < index[1]);

        if(M < tnew.length){
            iniM = Math.floor((tnew.length-M)/2);
            let incr = jnew[iniM] > jnew[iniM+M] ? -1 : 1;
            while((incr < 0 && jnew[iniM] > jnew[iniM+M]) 
                || (incr > 0 && jnew[iniM] < jnew[iniM+M])){
                iniM += incr;
            }
            if(jnew[iniM] < jnew[iniM+M+1]){
                iniM++;
            }
        }
        else{
            M = tnew.length-1;
        }    
        tpick = tnew.slice(iniM, M+iniM+1);
        jpick = jnew.slice(iniM, M+iniM+1);

        Plotly.addTraces(plotid, {x:tpick, y:jpick, name:"Peak Positions", mode:"markers",
        marker:{symbol:"circle-open", size:15, color:"black"}});
    }
    else if(dbl){
        let tpick2 = Array.from(tpick, t => t+td);
        let tpall = tpick.concat(tpick2);
        let tdmin = (raddelay+2*Lret/2/gam2)/CC*10**15;
        tpall.sort((a, b) => a-b);
        tpall.push(tpall[tpall.length-1]+tdmin);
        let tnew = [], tplot = [];
        for(let n = 0; n < tpall.length-1; n++){
            let tinv = tpall[n+1]-tpall[n];
            if(tinv < tdmin){
                if(tinv > radpermin){
                    tnew.push([tpall[n], tpall[n+1]]);
                    tplot.push(tpall[n]);
                    tplot.push(tpall[n+1]);
                }
                else{
                    tnew.push((tpall[n+1]+tpall[n])/2);
                    tplot.push((tpall[n+1]+tpall[n])/2);
                }
                n++;    
            }
            else{
                tnew.push(tpall[n]);
                tplot.push(tpall[n]);
            }
        }
        let jplot = Array.from(tplot, t => GetParabolic(tpick, jpick, t));
        Plotly.addTraces(plotid, {x:tplot, y:jplot, name:"Peak Positions", mode:"markers",
        marker:{symbol:"circle-open", size:15, color:"black"}});       
        tpick = tnew;
        M = tpick.length-1;
    }

    let zini = -(M-1)*segobj[SegPrmsLabel.interval]*0.5-Lrad*0.5;
    let simple = false;

    // fill with 0 field at entrace
//    zini -= lu*1.5;
//    zini = GenerateMPField(1, lu, 0, zini, dzbase, true, z, bx, by);   

    let pol = 1, pfactor, Kret, Nradr = Nrad, Kr = K, raddelayr;
    for(let m = 0; m < M; m++){
        let luretr = luret;
        let Lretr = Lret;
        if(m == norpos){
            luretr = luretch;
            Lretr = Lchc;
        } 
        if(isempt){
            let Lint = segobj[SegPrmsLabel.interval];
            pfactor = [];
            for(let i = 1; i >= 0; i--){
                if((i == 1 && m == 0) || (i == 0 && m == M-1)){
                    pfactor.push(0.5);
                    continue;
                }
                let delay = (tpick[M-m+i]-tpick[M-m-1+i])*1e-15*CC;
                let lamhat = delay/(lu/2/gam2);
                let alpha = GetEndFactor(lamhat, Lint, lu, K, (-1)**m);                
                pfactor.push(alpha);
            }
            Kret = 0;
        }
        else{
            let delay, krd = [0,0], krdelay = [0,0];
            for(let j = 0; j < 2; j++){
                if(Array.isArray(tpick[M-m-j])){
                    let tdd = (tpick[M-m-j][1]-tpick[M-m-j][0])*1e-15*CC;
                    krd[j] = tdd-lu/2/gam2;
                    if(krd[j] < 0){
                        Alert("Delay at "+(M-m-j).toString()+"-th twin interval too narrow.");
                        return;    
                    }
                    krd[j] = Math.sqrt(4*gam2*krd[j]/lu);
                    krdelay[j] = lu*(12+5*krd[j]*krd[j])/16/gam2;
                }    
            }
            if(Array.isArray(tpick[M-m]) && Array.isArray(tpick[M-m-1])){
                delay = (tpick[M-m][0]-tpick[M-m-1][1])*1e-15*CC;                
                Nradr = 2;
                simple = true;
                Kr = -krd[0];
                raddelayr = (krdelay[0]+krdelay[1])/2;
            }
            else if(Array.isArray(tpick[M-m])){
                delay = (tpick[M-m][0]-tpick[M-m-1])*1e-15*CC;
                Nradr = 2;
                simple = true;
                Kr = -krd[0];
                raddelayr = (krdelay[0]+raddelay)/2;
            }
            else if(Array.isArray(tpick[M-m-1])){
                delay = (tpick[M-m]-tpick[M-m-1][1])*1e-15*CC;
                Nradr = 1;
                Kr = K;
                raddelayr = (raddelay+krdelay[1])/2;
                simple = false;
            }
            else{
                delay = (tpick[M-m]-tpick[M-m-1])*1e-15*CC;
                Nradr = Nrad;
                raddelayr = raddelay;
                Kr = K;
                simple = false;
            }
            if(m == norpos){
                Kret = delay*norsl-raddelayr-pdelay-Lretr/2/gam2;
            }
            else{
                Kret = delay-raddelayr-pdelay-Lretr/2/gam2;
            }
            if(Kret < 0){
                Alert("Delay at "+(M-m).toString()+"-th interval too narrow.");
                return;    
            }
            if(epret){
                Kret = Math.sqrt(Kret*gam2/luret/(5.0/16.0+7.0/18.0));
            }
            else{
                Kret = Math.sqrt(Kret*gam2/luretr/(5.0/16.0));
            }
        }
        if(flip){
            if(dbl){
                pol = (-1)**(Math.floor(m/2));
            }
            else{
                pol = (-1)**m;
            }

        }
        Kret *= pol;

        // GenerateMPField(Nper, lu, K, zini, dzbase, symm, z, bx, by, pfactor, simple = false)
        if(isempt){
            zini = GenerateMPField(Nradr, lu, Kr, zini, dzbase, symm, z, bx, by, pfactor);
        }
        else{
            zini = GenerateMPField(Nradr, lu, Kr, zini, dzbase, symm, z, bx, by, null, simple);
        }
        if(Kpret > 0){
            zini = GenerateMPField(1, luret, Kpret*pol, zini, dzbase, true, z, bx, by, null);
            zini = GenerateMPField(Nradr, lu, Kr, zini, dzbase, symm, z, bx, by, null);
        }
        if(m < M-1){
            if(epret){
                let bxy = [bx, by];
                zini = GenerateHelicalRetarder(Lret, Kret, zini, dzbase, z, bxy);
            }
            else{
                zini = GenerateMPField(1, luretr, Kret, zini, dzbase, true, z, bx, by, null);
            }
        }
        let nums = z.length-secno.length;
        for(let i = 0; i < nums; i++){
            secno.push(m);
        }
    }

    z.push(zini); bx.push(0); by.push(0); secno.push(M-1);
    let outobj = {
        Output:{dimension:1, titles:["z", "Bx", "By"], 
        units:["m", "T", "T", "-"], data:[z, bx, by]}
    };
    /*
    if(issecno){
        outobj.Output.titles.push("Section");
        outobj.Output.units.push("-");
        data.Output.units.push(secno);
    }*/
    let outres = JSON.stringify(outobj);
    SIMPLEX.postprocessor.SetImportFiles([{name:"field4sc3.json"}]);
    SIMPLEX.postprocessor.LoadOutputFile(outres); 
}

function CreateMenuItems()
{
    let data = "";
    for(let n = 0; n < SIMPLEX.allmenus.length; n++){
        data += n.toString()+"\t"+SIMPLEX.allmenus[n]+"\n";
    }
    let blob = new Blob([data], {type:"text/plain"});
    let link = document.createElement("a");
    link.href = window.URL.createObjectURL(blob);
    link.download = "calc_types.txt";
    link.click();
    link.remove();
}

//-------------------------
// utility functions to generate header file
//-------------------------
const MapCont = "map<string, tuple<int, string>>";
const MapLabel = "const map<string, tuple<int, string>> ";
const CalcTypeLabel = "Calculation Type";
const AccTypeCaption = "Accelerator Type";
const SrcTypeCaption = "Light Source Type";
const EditMaterial = "Filter/Absorber Material";
const EditMagnet = "Magnet Configurations";
const EditAccuracy = "Numerical Accuracy";
const EditUnitsLabel = "Units for Data Import";
const EditMPIConfig = "Parallel Computing";
const EditPhaseErrConfig = "Phase Error Evaluation";
const EditFiltPlotConfig = "Transmission/Absorption Rate Plot";
const HelpReference  = "Open Reference Manual";
const HelpAbout = "About SPECTRA";

const SrcTypeLabel = {
    LIN_UND: LIN_UND_Label,
    VERTICAL_UND: VERTICAL_UND_Label,
    HELICAL_UND: HELICAL_UND_Label,
    ELLIPTIC_UND: ELLIPTIC_UND_Label,
    FIGURE8_UND: FIGURE8_UND_Label,
    VFIGURE8_UND: VFIGURE8_UND_Label,
    MULTI_HARM_UND: MULTI_HARM_UND_Label,
    BM: BM_Label,
    WIGGLER: WIGGLER_Label,
    EMPW: EMPW_Label,
    WLEN_SHIFTER: WLEN_SHIFTER_Label,
    FIELDMAP3D: FIELDMAP3D_Label,
    CUSTOM_PERIODIC: CUSTOM_PERIODIC_Label,
    CUSTOM: CUSTOM_Label
};

function FormatCSVString(strobj, crnum, is4enum)
{
    let nitems = 0;
    let ist = 0, bef, aft;
    while(true){
        ist = strobj.indexOf(", ", ist);
        if(ist == -1){
            break;
        }
        ist++;
        nitems++;
        if(nitems%crnum == 0){
            bef = strobj.slice(0, ist-1);
            aft = strobj.slice(ist-1);
            if(is4enum){
                strobj = bef+aft.replace(", ", ",\n\t\t");
                ist +=2 ;    
            }
            else{
                strobj = bef+aft.replace(", ", ",\n\t");
                ist++;    
            }
        }
    }
    return is4enum ? "\t"+strobj : "{\n\t"+strobj+"\n};\n";
}

function FormatCppVector(type)
{
    return "const vector<"+type+"> ";
}

function FormatCppVectorDouble(type)
{
    return "const vector<vector<"+type+">> ";
}

function FormatTuple(label, index, fmt)
{
    return '{"'+label+'", '+"tuple<int, string> ("+index+', "'+fmt+'")}';
}

function FormatConst(labelobj, prefix = "")
{
    let data = "";
    for(let i = 0; i < labelobj.length; i++){
        let keys = Object.keys(labelobj[i]);
        data += prefix+"const string "+keys[0]+" = "+'"'+labelobj[i][keys[0]]+'"'+";\n"
    }
    return data;
}

function FormatMaterials(materials)
{
    let data = "";
    let keys = Object.keys(materials);
    for(let i = 0; i < keys.length; i++){
        data += '\t{"'+keys[i]+'", tuple<double, vector<double>> ('+ 
            materials[keys[i]].dens+", {";
        for(let j = 0; j < materials[keys[i]].comp.length; j++){
            if(j > 0){
                data += ", "
            }
            data += materials[keys[i]].comp[j][0]+", "
                +materials[keys[i]].comp[j][1];
        }
        data += "})}";
        if(i < keys.length-1){
            data += ",\n"
        }
    }
    return data;
}

function GenerateHeaderFile()
{
    let data = "";
    data += "// ---------------------------------------------------\n";
    data += "// automatically generated by SPECTRA GUI, do not edit\n";
    data += "// ---------------------------------------------------\n\n";
    data += "#ifndef spectra_input_h\n#define spectra_input_h\n\n";
    data += "#include <string>\n";
    data += "#include <map>\n";
    data += "#include <tuple>\n";
    data += "#include <vector>\n";
    data += "using namespace std;\n\n";

    let scanprms = 4;
    // ScanPrmsLabel.initial, ScanPrmsLabel.final, ScanPrmsLabel.points/ScanPrmsLabel.interv, ScanPrmsLabel.iniser

    let constlabels = [
        {AccLabel:AccLabel}, 
        {SrcLabel:SrcLabel}, 
        {ConfigLabel:ConfigLabel},
        {SimplifiedLabel:SimplifiedLabel},
        {FMaterialLabel:FMaterialLabel},
        {InputLabel:InputLabel},
        {OutputLabel:OutputLabel},
        {OutFileLabel:OutFileLabel},
        {Link2DLabel:Link2DLabel},
        {TypeLabel:TypeLabel},
        {ScanLabel:ScanLabel},
        {BundleScanlabel:BundleScanlabel},
        {OrgTypeLabel:OrgTypeLabel},
        {NumberLabel:NumberLabel},
        {IntegerLabel:IntegerLabel},
        {TitleLabel:TitleLabel},
        {DataLabel:DataLabel},
        {GridLabel:GridLabel},
        {BoolLabel:BoolLabel},
        {StringLabel:StringLabel},
        {SelectionLabel:SelectionLabel},
        {ArrayLabel:ArrayLabel},
        {TimeLabel:TimeLabel},
        {NormCurrLabel:NormCurrLabel},
        {BeamCurrLabel:BeamCurrLabel},
        {EdevLabel:EdevLabel},
        {ZLabel:ZLabel},
        {BxLabel:BxLabel},
        {ByLabel:ByLabel},
        {GapLabel:GapLabel},
        {EnergyLabel:EnergyLabel},
        {TransmLabel:TransmLabel},
        {OutFormat:OutFormat},
        {PPBetaLabel:PPBetaLabel},
        {PPFDlabel:PPFDlabel},
        {PP1stIntLabel:PP1stIntLabel},
        {PP2ndIntLabel:PP2ndIntLabel},
        {PPPhaseErrLabel:PPPhaseErrLabel},
        {PPRedFlux:PPRedFlux},
        {PPTransLabel:PPTransLabel},
        {PPAbsLabel:PPAbsLabel},
        {ScanPrmItems:scanprms.toString()},
        {CalcStatusLabel:CalcStatusLabel},
        {Fin1ScanLabel:Fin1ScanLabel},
        {ScanOutLabel:ScanOutLabel},
        {ErrorLabel:ErrorLabel},
        {WarningLabel:WarningLabel},
        {DataDimLabel:DataDimLabel},
        {DataTitlesLabel:DataTitlesLabel},
        {UnitsLabel:UnitsLabel},
        {VariablesLabel:VariablesLabel},
        {DetailsLabel:DetailsLabel},
        {RelateDataLabel:RelateDataLabel},
        {CMDResultLabel:CMDResultLabel},
        {CMDModalFluxLabel:CMDModalFluxLabel},
        {CMDFieldLabel:CMDFieldLabel},
        {CMDIntensityLabel:CMDIntensityLabel},
        {CMDCompareIntLabel:CMDCompareIntLabel},
        {CMDCompareXLabel:CMDCompareXLabel},
        {CMDCompareYLabel:CMDCompareYLabel},
        {CMDErrorLabel:CMDErrorLabel},
        {MaxOrderLabel:MaxOrderLabel},
        {WavelengthLabel:WavelengthLabel},
        {SrcSizeLabel:SrcSizeLabel},
        {OrderLabel:OrderLabel},
        {AmplitudeReLabel:AmplitudeReLabel},
        {AmplitudeImLabel:AmplitudeImLabel},
        {AmplitudeVReLabel:AmplitudeVReLabel},
        {AmplitudeVImLabel:AmplitudeVImLabel},
        {AmplitudeIndexReLabel:AmplitudeIndexReLabel},
        {AmplitudeIndexImLabel:AmplitudeIndexImLabel},        
        {NormFactorLabel:NormFactorLabel},
        {FluxCMDLabel:FluxCMDLabel},
        {MatrixErrLabel:MatrixErrLabel},
        {FluxErrLabel:FluxErrLabel},
        {WignerErrLabel:WignerErrLabel},
        {FELCurrProfile:FELCurrProfile},
        {FELEtProfile:FELEtProfile},
        {FELCurrProfileR56:FELCurrProfileR56},
        {FELEtProfileR56:FELEtProfileR56},
        {FELBunchFactor:FELBunchFactor},
        {FELPulseEnergy:FELPulseEnergy},
        {FELEfield:FELEfield},
        {FELInstPower:FELInstPower},
        {FELSpectrum:FELSpectrum},
        {FELSecIdxLabel:FELSecIdxLabel},
        {AccuracyLabel:AccuracyLabel},
        {SeedWavelLabel:SeedWavelLabel},
        {SeedFluxLabel:SeedFluxLabel},
        {SeedPhaseLabel:SeedPhaseLabel},
        {PrePLabel:PrePLabel}
    ];

    data += "// labels for parameters and data import\n"
            +FormatConst(constlabels)+"\n";

    const AccTypeLabel = {
        RING: RINGLabel,
        LINAC: LINACLabel
    };
            
    let acctypelabels = [];
    let acckeys = Object.keys(AccTypeLabel);
    for(let i = 0; i < acckeys.length; i++){
        let obj = {};
        obj[acckeys[i]] = AccTypeLabel[acckeys[i]];
        acctypelabels.push(obj);
    }
    data += "// labels for Accelerator types\n"
            +FormatConst(acctypelabels)+"\n";
            
    let idtypelabels = [];
    let idkeys = Object.keys(SrcTypeLabel);
    for(let i = 0; i < idkeys.length; i++){
        let obj = {};
        obj[idkeys[i]] = SrcTypeLabel[idkeys[i]];
        idtypelabels.push(obj);
    }
    data += "// labels for ID types\n"
            +FormatConst(idtypelabels)+"\n";

    let selections = [
        {AutomaticLabel:AutomaticLabel}, 
        {DefaultLabel:DefaultLabel},
        {NoneLabel:NoneLabel}, 
        {GaussianLabel:GaussianLabel}, 
        {ImportPaticleLabel:ImportPaticleLabel}, 
        {CurrProfLabel:CurrProfLabel}, 
        {EtProfLabel:EtProfLabel}, 
        {CustomLabel:CustomLabel}, 
        {EntranceLabel:EntranceLabel}, 
        {CenterLabel:CenterLabel}, 
        {ExitLabel:ExitLabel}, 
        {BxOnlyLabel:BxOnlyLabel}, 
        {ByOnlyLabel:ByOnlyLabel}, 
        {BothLabel:BothLabel}, 
        {IdenticalLabel:IdenticalLabel}, 
        {ImpGapTableLabel:ImpGapTableLabel}, 
        {SwapBxyLabel:SwapBxyLabel}, 
        {FlipBxLabel:FlipBxLabel}, 
        {FlipByLabel:FlipByLabel},
        {AntiSymmLabel:AntiSymmLabel},
        {SymmLabel:SymmLabel},
        {FixedSlitLabel:FixedSlitLabel}, 
        {NormSlitLabel:NormSlitLabel}, 
        {GenFilterLabel:GenFilterLabel}, 
        {BPFGaussianLabel:BPFGaussianLabel}, 
        {BPFBoxCarLabel:BPFBoxCarLabel}, 
        {LinearLabel:LinearLabel}, 
        {LogLabel:LogLabel}, 
        {ArbPositionsLabel:ArbPositionsLabel},
        {ObsPointDist:ObsPointDist},
        {ObsPointAngle:ObsPointAngle},
        {JSONOnly:JSONOnly},
        {ASCIIOnly:ASCIIOnly},
        {BothFormat:BothFormat},
        {BinaryOnly:BinaryOnly},
        {XOnly:XOnly},
        {YOnly:YOnly},
        {FELPrebunchedLabel:FELPrebunchedLabel},
        {FELSeedLabel:FELSeedLabel},
        {FELSeedCustomLabel:FELSeedCustomLabel},
        {FELCPSeedLabel:FELCPSeedLabel},
        {FELDblSeedLabel:FELDblSeedLabel},
        {FELReuseLabel:FELReuseLabel},
        {PhaseErrZPole:PhaseErrZPole},
        {PhaseErrZPos:PhaseErrZPos}
    ];
    data += "// labels for selections\n"
        +FormatConst(selections)+"\n";

    let calclabels = {}
    Object.keys(CalcLabels).forEach(type => {
        calclabels = Object.assign(calclabels, CalcLabels[type]);
    });
    let menuitems = [];
    let menukeys = Object.keys(calclabels);
    for(let i = 0; i < menukeys.length; i++){
        let obj = {};
        obj[menukeys[i]] = calclabels[menukeys[i]];
        menuitems.push(obj);
    }
    data += "// Menu items\nnamespace menu {\n"
            +FormatConst(menuitems, "\t")+"}\n\n";

    data += "// Built-in Filter Materials\n"
            +"const map<string, tuple<double, vector<double>>> FilterMaterials {\n"
            +FormatMaterials(FilterMaterial)+"\n};\n\n"            

    let crnumv = 8, crnums = 4;
    let update = [];
    for(let j = 0; j < UpdateScans.length; j++){
        update.push("\""+UpdateScans[j]+"\"");
    }
    data += "// labels to force update for scan option\n";
    data += FormatCppVector("string")+" UpdateScans "+FormatCSVString(update.join(", "), crnumv, false)+"\n"

    let hdrorg = [
        {enum:[], str:[], strsimp:[], def:[]}, // 0: number
        {enum:[], str:[], strsimp:[], def:[]}, // 1: vector
        {enum:[], str:[], strsimp:[], def:[]}, // 2: boolean
        {enum:[], str:[], strsimp:[], def:[], select:[]}, // 3: selection
        {enum:[], str:[], strsimp:[], def:[]}, // 4: string
        {enum:[], str:[], strsimp:[]} // 5: plottable data
    ];

    let categsufs = {
        [AccLabel]: ["Acc", AccLabelOrder, AccPrmsLabel],
        [SrcLabel]: ["Src", SrcLabelOrder, SrcPrmsLabel],
        [ConfigLabel]: ["Conf", ConfigLabelOrder, ConfigPrmsLabel],
        [OutFileLabel]: ["Outfile", OutputOptionsOrder, OutputOptionsLabel],
        [AccuracyLabel]: ["Accuracy", AccuracyOptionsOrder, AccuracyOptionsLabel],
        [PrePLabel]: ["Preproc", PreProcessPrmOrder, PreProcessPrmLabel]
    };
    let keys = Object.keys(categsufs);

    let suf = ["Prm", "Vec", "Bool", "Sel", "Str", "Data"];
    let ctypes = ["double", "vector<double>", "bool", "string", "string", ""];
    // length of suf & ctypes should be the same

    let simplel = "Simple"
    let headers;
    let defvalues = {};
    let maplabels = [], mapsimples = [];
    for(let n = 0; n < keys.length; n++){
        headers =  CopyJSON(hdrorg);

        DumpObjHeaderOption(categsufs[keys[n]], SIMPLEX.default[keys[n]], headers);
        headers = ConcatHeaderObjs(suf, ctypes, categsufs[keys[n]][0], simplel, headers, crnumv, crnums, defvalues);
        data += "// "+keys[n]+"\n";
        data += headers+"\n";

        maplabels.push(categsufs[keys[n]][0]);
        mapsimples.push(categsufs[keys[n]][0]+simplel);
    }

    data = data.replaceAll("null", "0");

    data += "// import data format\n";
    data += ExportAsciiFormat();

    let enumkeys = [], keystrs = [];
    for(let j = 0; j < keys.length; j++){
        enumkeys.push(categsufs[keys[j]][0]+"_");
        keystrs.push("\""+keys[j]+"\"");
    }
    enumkeys[0] += " = 0";
    enumkeys.push("Categories");

    data += "// parameter categories\n";
    data += "enum CategoryOrder "+FormatCSVString(enumkeys.join(", "), crnumv, false)+"\n"

    data += FormatCppVector("string")+" CategoryNames "+FormatCSVString(keystrs.join(", "), crnumv, false)+"\n"

    data += FormatCppVector(MapCont)+" ParameterFullNames "+FormatCSVString(maplabels.join(", "), crnumv, false)+"\n";
    data += FormatCppVector(MapCont)+" ParameterSimples "+FormatCSVString(mapsimples.join(", "), crnumv, false)+"\n";

    let defaults = new Array(suf.length);
    for(let n = 0; n < suf.length; n++){
        if(ctypes[n] == ""){
            continue;
        }
        defaults[n] = FormatCppVectorDouble(ctypes[n])+" Default"+suf[n]+" "+FormatCSVString(defvalues[suf[n]].join(", "), crnumv, false);
    } 
    data += defaults.join("\n");

    data += ExportObsoleteLabels(crnums);

    data += "const int JSONIndent = "+JSONIndent+";\n\n";
    
    data += "#endif"

    let blob = new Blob([data], {type:"text/plain"});
    let link = document.createElement("a");
    link.href = window.URL.createObjectURL(blob);
    link.download = "spectra_input.h";
    link.click();
    link.remove();
}

function ExportObsoleteLabels(crnum)
{
    let labels = Array.from(PrmTableKeys);
    labels.push(OptionLabel);

    let obslabels = [];
    labels.forEach(prm => {
        obslabels.push('"'+prm+'"');
    });

    let data = FormatCppVector("string")+"ObsoleteLabels "
        +FormatCSVString(obslabels.join(", "), crnum)+"\n"

    return data;
}

function ExportAsciiFormat()
{
    let labels = [
        [CustomCurrent, "currdata"],
        [CustomEt, "Etdata"],
        [CustomField, "fvsz"],
        [CustomPeriod, "fvsz1per"],
        [ImportGapField, "gaptbl"],
        [CustomFilter, "fcustom"],
        [CustomDepth, "depthdata"],
        [SeedSpectrum, "seedspec"]
    ];
    let objs = [[], []];
    for(let i = 0; i < labels.length; i++){
        for(let j = 0; j < labels[i].length; j++){
            let tplc = '{"'+labels[i][j]+'"'+", tuple<int, vector<string>> ("+AsciiFormats[labels[i][0]].dim;
            let strbr = JSON.stringify(AsciiFormats[labels[i][0]].titles);
            let tmp = strbr.replace("[", "").replace("]", "");
            tplc += ", {"+tmp+"})}";
            objs[j].push(tplc);    
        }
    }
    let data = "const map<string, tuple<int, vector<string>>> DataFormat {\n\t"+objs[0].join(",\n\t")+"\n};\n\n";
    data += "const map<string, tuple<int, vector<string>>> DataFormatSimple {\n\t"+objs[1].join(",\n\t")+"\n};\n\n";
    return data;
}

function DumpObjHeaderOption(categobjs, obj, hdrdata)
{
    let categ = categobjs[0];
    let orders = categobjs[1];
    let labels = categobjs[2];

    let hdridx, isstr, fmt;
    for(let i = 0; i < orders.length; i++){
        isstr = false;
        if(orders[i] == SeparatorLabel){
            continue;
        }
        let label = labels[orders[i]][1];
        if(label == SimpleLabel){
            continue;
        }
        else if(label == null){
            continue;
        }
        else if(Array.isArray(label)){
            if(label[0] == null){
                continue;
            }
        }
        if(label == PlotObjLabel){
            hdridx = 5; // data
            fmt = DataLabel;
        }
        else if(label == GridLabel){
            hdridx = 5; // data
            fmt = GridLabel;
        }
        else if(Array.isArray(label)){
            if(labels[orders[i]].length > 2 && labels[orders[i]][2] == SelectionLabel){
                hdridx = 3; // selection
                let brac = [];
                for(let j = 0; j < label.length; j++){
                    brac.push('"'+label[j]+'"');
                }
                hdrdata[hdridx].select.push(brac);
                isstr = true;
                fmt = SelectionLabel;    
            }
            else{
                hdridx = 1; // vertor
                fmt = ArrayLabel;
            }
        }
        else if(typeof label == "boolean"){
            hdridx = 2; // boolean
            fmt = BoolLabel;
        }
        else{
            if(typeof obj[label] == "object"){
                console.log("Invalid format for "+labels[orders[i]][0]);
                continue;
            }
            if(typeof label == "number"){
                hdridx = 0; // number
                fmt = NumberLabel;
            }
            else{
                hdridx = 4; // string
                fmt = StringLabel;
                isstr = true;
            }
        }
        let prmname = orders[i];
        if(prmname == "type"){
            prmname = categ+prmname;
        }
        hdrdata[hdridx].enum.push(prmname+"_");
        hdrdata[hdridx].str.push(FormatTuple(labels[orders[i]][0], prmname+"_", fmt));
        hdrdata[hdridx].strsimp.push(FormatTuple(prmname, prmname+"_", fmt));

        if(label == FileLabel 
                || label == FolderLabel){
            hdrdata[hdridx].def.push('""');
        }
        else if(hdridx != 5){
            if(isstr){
                hdrdata[hdridx].def.push('"'+obj[labels[orders[i]][0]].toString()+'"');
            }
            else if(fmt == ArrayLabel){
                hdrdata[hdridx].def.push(obj[labels[orders[i]][0]]);
            }
            else{
                hdrdata[hdridx].def.push(obj[labels[orders[i]][0]].toString());
            }
        }
    }
}

function ConcatHeaderObjs(suf, ctypes, categ, simplel, hdrdata, crnumv, crnums, defvalues)
{
    let enumcont = [];
    let strcont = [];
    let strsimcont = [];
    let defconts = [];
    let defcont;
    let tmp;

    let label = MapLabel+categ;
    let nlabel = "Num"+categ;
    let deflabel = "Def"+categ;
    let types = [];
    for(let n = 0; n < ctypes.length; n++){
        types.push(FormatCppVector(ctypes[n]));

    }
    let numlabels = [];
    let defs = [];
    for(let i = 0; i < suf.length; i++){
        numlabels.push(nlabel+suf[i]);
        defs.push(types[i]+deflabel+suf[i]+" ");
        if(!defvalues.hasOwnProperty(suf[i])){
            defvalues[suf[i]] = [];
        }
        defvalues[suf[i]].push(deflabel+suf[i]);
    }

    for(let n = 0; n < hdrdata.length; n++){
        if(hdrdata[n].enum.length == 0){
            if(n < 5){
                defconts.push(defs[n]+"{};\n");
            }
            continue;
        }
        hdrdata[n].enum[0] += " = 0";
        hdrdata[n].enum.push(numlabels[n]);

        tmp = hdrdata[n].enum.join(", ");
        enumcont.push(FormatCSVString(tmp, crnumv, true));

        strcont.push(hdrdata[n].str.join(",\n\t"));
        strsimcont.push(hdrdata[n].strsimp.join(",\n\t"));

        if(hdrdata[n].hasOwnProperty("def")){
            let crnum = n == 0 || n == 1 || n == 2 ? crnumv : crnums;
            if(n == 1){
                let tmpbra = [];
                for(let i = 0; i < hdrdata[n].def.length; i++){
                    tmpbra.push("{"+hdrdata[n].def[i][0]+", "+hdrdata[n].def[i][1]+"}");
                }
                tmp = tmpbra.join(", ");
                defcont = defs[n]+FormatCSVString(tmp, crnum*2, false);
            }
            else{
                tmp = hdrdata[n].def.join(", ");
                defcont = defs[n]+FormatCSVString(tmp, crnum, false);
            }
            defconts.push(defcont);
        }
    }

    enumcont = "enum "+categ+"Index {\n"+enumcont.join(",\n")+"\n};\n";

    let strf = label+" {\n\t"+strcont.join(",\n\t")+"\n};\n";
    let strsimf = label+simplel+" {\n\t"+strsimcont.join(",\n\t")+"\n};\n";

    let data = [enumcont, strf, strsimf, defconts.join("\n")];
    return data.join("\n");
}

//-------------------------
// generate help file
//-------------------------
var header_tags = ["h1", "h2", "h3", "h4", "h5", "h6"];
var espcape_chars = ["&lambda;","&gamma","&epsilon;","&eta;","&beta;","&sigma;","&Sigma;"];

// utility functions
function FormatHTML(htmlstr)
{
    let formathtml = htmlstr
        .replace(/<tbody>/g, "<tbody>\n\n")
        .replace(/<tr>/g, "<tr>\n")
        .replace(/<\/tr>/g, "</tr>\n")
        .replace(/<\/td>/g, "</td>\n")
        .replace(/<\/h1>/g, "</h1>\n")
        .replace(/<\/h2>/g, "</h2>\n")
        .replace(/<\/h3>/g, "</h3>\n")
        .replace(/<\/h4>/g, "</h4>\n")
        .replace(/<\/h5>/g, "</h5>\n")
        .replace(/<\/h6>/g, "</h6>\n")
        .replace(/<p>/g, "\n<p>")
        .replace(/<\/p>/g, "</p>\n")
        .replace(/<\/table>/g, "</table>\n\n");
    return formathtml;
}

function SetRemarks(categ, captions)
{
    let data ="";
    for(let j = 0; j < captions.length; j++){
        let capp = document.createElement("p");
        capp.innerHTML = captions[j];
        capp.id  = categ+(j+1).toString();
        data += capp.outerHTML;
    }
    return data;
}

function GetQString(str)
{
    return "\""+str+"\"";
}

function GetLink(href, caption, isel)
{
    let link = document.createElement("a");
    link.href = "#"+href;
    link.innerHTML = caption;
    if(isel){
        return link;
    }
    return link.outerHTML;
}

function RetrieveEscapeChars(label)
{
    let fchars = [];
    let iini, ifin = 0;
    do{
        iini = label.indexOf("&", ifin);
        if(iini >= 0){
            ifin = label.indexOf(";", iini);
            if(ifin < 0){
                ifin = iini+1;
                continue;
            }
            let fchar = label.substring(iini , ifin+1);
            if(fchars.indexOf(fchar) < 0){
                fchars.push(fchar);
            }
        }    
    } while(iini >= 0);
    return fchars;
}

function RetrieveAllEscapeChars(prmlabels)
{
    let escchars = [];
    for(let j = 0; j < prmlabels.length; j++){
        let labels = Object.values(prmlabels[j]);
        for(let i = 0; i < labels.length; i++){
            let fchars = RetrieveEscapeChars(labels[i][0]);
            for(let k = 0; k < fchars.length; k++){
                if(escchars.indexOf(fchars[k]) < 0){
                    escchars.push(fchars[k]);
                }    
            }
        }
    }
    return escchars;
}

function ReplaceSpecialCharacters(espchars, org)
{
    let ret = org;
    let div = document.createElement("div");
    for(let j = 0; j < espchars.length; j++){
        div.innerHTML = espchars[j];
        let spchar = div.innerHTML;
        while(ret.indexOf(spchar) >= 0){
            ret = ret.replace(spchar, espchars[j]);
        }    
    }
    return ret;
}

function WriteParagraph(phrases)
{
    let data = "";
    for(let j = 1; j < phrases.length; j++){
        let p = document.createElement("p");
        p.innerHTML = phrases[j];
        data += p.outerHTML;
    }
    return data;
}

function WriteListedItem(items, isnumber)
{
    let data;
    let ol = document.createElement(isnumber?"ol":"ul");
    for(let j = 1; j < items.length; j++){
        let li = document.createElement("li");
        li.innerHTML = items[j];
        ol.appendChild(li);
    }
    data = ol.outerHTML;
    return data;
}

function WriteFigure(src, figcaption, intbl)
{
    let fig = document.createElement("figure");
    fig.id = src;
    let img = document.createElement("img");
    img.src = src;
    if(intbl){
        img.style.width = "100%";
    }
    let caption = document.createElement("figcaption");
    caption.innerHTML = figcaption;
    fig.appendChild(img);
    fig.appendChild(caption);
    return fig.outerHTML;
}

function WriteObject(layer, obj)
{
    if(obj.hasOwnProperty("type")){
        if(obj.type == "figure"){
            return WriteFigure(obj.src, obj.caption, false);
        }
        else{
            return "ERROR";
        }
    }
    let value;
    let data = "";
    if(Array.isArray(obj) == true){
        value = CopyJSON(obj);
    }
    else{
        let key = Object.keys(obj)[0];
        value = Object.values(obj)[0];
    
        layer = Math.min(layer, header_tags.length-1);
        let hdr = document.createElement(header_tags[layer]);
        hdr.innerHTML = key;
        hdr.id = key;
        data += hdr.outerHTML;
    
        if(typeof value == "string" && value.indexOf("@") >= 0){
            data += value;
            return data;
        }
        else if(Array.isArray(value) == false){
            data += "Error";
            alert("Error"+value);
            return data;
        }   
    }

    if(value[0] == "Paragraph"){
        data += WriteParagraph(value);
        return data;
    }
    else if(value[0] == "NumberedItem"){
        data += WriteListedItem(value, true);
        return data;
    }
    else if(value[0] == "ListedItem"){
        data += WriteListedItem(value, false);
        return data;
    }

    for(let j = 0; j < value.length; j++){
        if(typeof value[j] != "string"){
            data += WriteObject(layer+1, value[j]);
        }
        else if(value[j].indexOf("<img") >= 0){
            data += value[j];
        }
        else{
            let p = document.createElement("p");
            p.innerHTML = value[j];
            data += p.outerHTML;
        }
    }
    return data;
}

function GetTable(captext, titles, data)
{
    let cell, rows = [];
    let table = document.createElement("table");

    if(captext != ""){
        let caption = document.createElement("caption");
        caption.innerHTML = captext;
        table.caption = caption;    
    }

    rows.push(table.insertRow(-1)); 
    for(let j = 0; j < titles.length; j++){
        cell = rows[rows.length-1].insertCell(-1);
        cell.innerHTML = titles[j];    
        cell.className = " title";
    }

    for(let j = 0; j < data.length; j++){
        rows.push(table.insertRow(-1));
        for(let i = 0; i < titles.length; i++){
            cell = rows[rows.length-1].insertCell(-1);
            if((typeof data[j][i]) == "string"){
                cell.innerHTML = data[j][i];
            }
            else{
                cell.innerHTML = WriteObject(0, data[j][i]);
            }
        }
        if(data[j].length > titles.length){
            // set the id of this cell
            cell.id = data[j][titles.length]
        }
    }
    let retstr = table.outerHTML;
    return retstr;    
}

function GetMenuCommand(menus)
{
    let qmenus = [];
    for(let j = 0; j < menus.length; j++){
        qmenus.push("["+menus[j]+"]");
    }
    return qmenus.join("-");
}

function GetDirectPara(str)
{
    let div = document.createElement("div");
    div.innerHTML = "<pre><code>"+str+"</code></pre>";
    div.className = "direct";
    return div.outerHTML;
}

function GetTableBody(tblstr, ishead, isfoot)
{
    let tblinner = tblstr;
    if(!ishead){
        tblinner = tblinner
            .replace("<table>", "")
            .replace("<tbody>", "");
    }
    if(!isfoot){
        tblinner = tblinner
            .replace("</table>", "")
            .replace("</tbody>", "");
    }
    return tblinner;
}

// main body
var chapters = {
    copyright: "Copyright Notice",
    intro: "Introduction",
    gui: "Operation of the GUI",
    prmlist: "Parameter List",
    calcsetup: "Calculation Setup",
    spcalc: "Advanced Functions",
    format: "File Format",
    spusage: "Special Usage",
    ref: "References",
    ack: "Acknowledgements"
}

var sections = {
    overview: "Overview",
    start: "Getting Started",
    main: "Main Parameters",
    postproc: "Post-Processing",
    preproc: "Pre-Processing",
    dataimp: "Data Import",
    plotlyedit: "Edit the Plot",
    json: "JSON Format",
    compplot: "Comparative Plot",
    mdplot: "Plotting 3/4-Dimensional Data",
    scan: "Scanning a Parameter",
    ascii: "Export/Download as ASCII",
    donwload: "Download Output File",
    prmset : PSNameLabel,
    setupdlg: "Setup Dialogs",
    outitems: "Output Items",
    ppcomp: "Parallel Computing",
    input: "Input Format",
    output: "Output Format",
    webapp: "Web-Application Mode",
    binary: "Binary Format for the Modal Profile",
    separa: "Separability",
    degcoh: "Degree of Spatial Coherence",
    phaseerr: "Analytical Method to Evaluate the Harmonic Intensity",
    kxyscan: "Notes on Scanning &epsilon;<sub>1st</sub>"
}

var refidx = {};
var referencelist = GetReference(refidx);

var help_body = 
[
    {
        [chapters.copyright]: [
            "Paragraph",
            "<em>Copyright 1998-2023 Takashi Tanaka</em>",
            "This software is free for use, however, the author retains the copyright to this software. It may be distributed in its entirety only and may not be included in any other product or be distributed as part of any commercial software.", 
            "This software is distributed with <em>NO WARRANTY OF ANY KIND</em>. Use at your own risk. The author is not responsible for any damage done by using this software and no compensation is made for it.",
            "This software has been developed, improved and maintained as voluntary work of the author. Even if problems and bugs are found, the author is not responsible for improvement of them or version up of the software.",
            "<em>If you are submitting articles to scientific journals with the results obtained by using this software, please cite the relevant references.</em> For details, refer to "+GetLink(chapters.intro, chapters.intro, false)+"."
        ]
    },
    {
        [chapters.intro]: [
            "This document describes the instruction to use the free software SPECTRA, a synchrotron radiation (SR) calculation code, and is located in \"[SPECTRA Home]/help\", where \"[SPECTRA Home]\" is the directory where SPECTRA has been installed. Brief explanations on the software and numerical implementation of SR calculation are given here, together with a simple instruction of how to get started. Note that <a href=\"https://www.mathjax.org/\">"+GetQString("MathJax")+"</a> javascript library is needed to correctly display the mathematical formulas, which is available online. If you need to read this document offline, "+GetQString("MathJax")+" should be installed in \"[SPECTRA Home]/help\" directory.",
            {
                [sections.overview]: [
                    "Paragraph",
                    "SPECTRA is a computer program to numerically evaluate the characteristics of radiation emitted from various synchrotron radiation (SR) sources, such as bending magnets and insertion devices (IDs, i.e., wigglers and undulators). In addition, SR sources with arbitrary magnetic fields are available by importing the magnetic field data prepared by the user. This makes it possible to estimate the real performance of the SR source by using the magnetic field distribution actually measured by field measurement instruments such as Hall probes.",
                    "To compute the characteristics of radiation and evaluate the performances of SR sources, a large number of parameters are required to specify the electron beam, light source, observation conditions, and options for numerical operations. SPECTRA is equipped with a fully graphical user interface (GUI) which facilitates configurations of them. In addition, a post-processor is included to verify the computation results graphically. Since version 11.0, the GUI is written based on the web technologies, i.e., HTML, CSS and Javascript, with the assistance of \"node.js\", \"Electron\" and \"Electron Builder\" to build a standalone application. For visualization of calculation results and imported data, \"Plotly\" library is used. Thanks to portability of these libraries, SPECTRA will run on most of the platforms such as Microsoft Windows, Macintosh OS X and Linux. SPECTRA does not require any other commercial software or libraries.",
                    "The numerical part of SPECTRA (\"solver\") is written in C++11 with the standard template library (STL). For bending magnets, wigglers and undulators, numerical implementation is based on the well-known expressions on SR, and the so-called far-field approximation is available for fast computation. For more accurate evaluation, expressions on SR in the near-field region are used for numerical computation. In this case, characteristics of SR emitted from both the ideal- and arbitrary-field devices can be calculated. For details of numerical implementation, refer to "+GetLink("spectrajsr", refidx.spectrajsr, false)+" and "+GetLink("spectrasri", refidx.spectrasri, false)+". The users who are publishing their results obtained with SPECTRA are kindly requested to cite "+GetLink("spectra11jsr", refidx.spectra11jsr, false)+".",
                    "Before ver. 7.2, the magnetic field was assumed to be constant in the transverse (x-y) plane. In other words, only the dipole components were taken into account. This considerably simplifies the numerical algorithm not only in the trajectory calculation but also in the spatial integration to take into account the finite electron beam emittance. In ver. 8.0, an arbitrary magnetic field has been supported to enable the evaluation of the effects due to quadrupole magnets between undulator segments and the undulator natural focusing, which would be significant for low-energy electrons. In ver. 9.0, an arbitrary electron bunch profile has been supported. The user can specify the longitudinal bunch profile, or import the macroparticle coordinates in the 6D phase space, which is usually created by the start-to-end simulation for accelerators.",
                    "In ver. 10.0, a new function to compute the photon flux density in the 4D phase space (x,x',y,y') has been implemented"+GetLink("refwigner", refidx.refwigner, false)+", which enables the rigorous estimation of the brilliance (brightness) of typical SR sources and the photon distribution at the source point to be utilized in other computer codes for ray-tracing simulations. Based on the phase-space density computed with this function, a numerical scheme to decompose the partially-coherent radiation into a number of coherent modes (coherent mode decomposition: CMD)"+GetLink("refcmd", refidx.refcmd, false)+" has been later implemented in version 10.1, which is explained in more detail "+GetLink(MenuLabels.CMD, "here", false)+". The users who are publishing their results obtained using these numerical schemes are kindly requested to cite the relevant references. Also implemented in ver. 10.1 is a function to compute the surface power density, which is convenient to compute the heat load on the inner wall of a vacuum chamber located near the SR source and exposed to SR with a shallow incident angle.",
                    "In ver. 11.0, the solver has been widely revised to be consistent with the C++11 standard and to facilitate the maintenance and bug fix. A new function has been also implemented to compute the volume power density; this is to evaluate the heat load of SR incident on an object, which gradually decays while it transmits the object. The output data will probably be used later for heat analysis of high heat-load components in the SR beamline based on the finite element method. In addition to the above revisions, three important upgrades have been made in ver. 11. First, the format of the input parameter file has been changed from the original (and thus not readable in other applications) one to JSON (JavaScript Object Notation) format. Because the output data is also given by a JSON file, it is now easy to communicate with other 3rd-party applications. Second, a number of functions implemented in SPECTRA have become available with python script. This makes it easy to do a batch job (repeat many calculations with different sets of parameters), which has been requested by many users. Third, SPECTRA can now work as a web application. For details, refer to "+GetLink(sections.webapp, sections.webapp, false)+"."
                ]
            },
            {
                [sections.start]: [
                    "NumberedItem",
                    "Open a parameter file by running "+GetMenuCommand([MenuLabels.file, MenuLabels.open])+" command, or run "+GetMenuCommand([MenuLabels.file, MenuLabels.new])+" command to start with a new parameter set.",
                    "Select the calculation type from submenus in "+GetMenuCommand([MenuLabels.calc])+".",
                    "Edit the parameters if necessary and specify the directory and data name to save the calculation results.",
                    "Run "+GetMenuCommand([MenuLabels.run, MenuLabels.start])+" command to start a calculation with current parameters.",
                    "A \"Progressbar\" appears to inform the calculation status.",
                    "To verify the calculation results after completion of the calculation, click "+GetQString(sections.postproc)+" tab, select the name of the output file and item(s) to check for visualization. Refer to "+GetLink(sections.postproc, sections.postproc, false)+" for details."
                ]
            }
        ]
    },
    {
        [chapters.gui]: [
            "SPECTRA GUI is composed of three tabbed panels entitled as "+GetQString(sections.main)+", "+GetQString(sections.preproc)+", and"+GetQString(sections.postproc)+", which are explained in what follows.",
            {
                [sections.main]: [
                    "The "+GetQString(sections.main)+" tabbed panel is composed of a number of subpanels entitled as "+GetQString(AccLabel)+", "+GetQString(SrcLabel)+", "+GetQString(ConfigLabel)+", "+GetQString(OutFileLabel)+", "+GetQString(CalcProcessLabel)+", and "+GetQString(CalcResultLabel)+". Note that the "+GetQString(AccLabel)+" and "+GetQString(SrcLabel)+" subpanels are always displayed, while the others are shown when necessary.",
                    {"type":"figure", "src":"main.png", "caption":"Example of the "+GetQString(sections.main)+" tabbed panel. Note that "+GetQString(CalcResultLabel)+" subpanel is not shown in this example."},
                    {
                        [AccLabel+" Subpanel"]: [
                            "Display and edit the parameters and numerical conditions related to the electron beam. For details, refer to "+GetLink(AccLabel, AccLabel+" "+chapters.prmlist, false)+"."
                        ]
                    },
                    {
                        [SrcLabel+" Subpanel"]: [
                            "Display and edit the parameters and numerical conditions related to the light source. For details, refer to "+GetLink(SrcLabel, SrcLabel+" "+chapters.prmlist, false)+"."
                        ]
                    },
                    {
                        [ConfigLabel+" Subpanel"]: [
                            "Display and edit the parameters and numerical conditions related to the observation of radiation. For details, refer to "+GetLink(ConfigLabel, ConfigLabel+" "+chapters.prmlist, false)+"."
                        ]
                    },
                    {
                        [OutFileLabel+" Subpanel"]: [
                            "Specify the path, name and format of the output file.",
                            "@outfile"
                        ]
                    },
                    {
                        [CalcProcessLabel+" Subpanel"]: [
                            "Display the status of a calculation in progress, or the list of "+GetLink(CalcProcessLabel, CalcProcessLabel, false)+". Click "+GetQString(CancelLabel)+" to stop the calculation currently running, "+GetQString(CancellAllLabel)+" to terminate all the calculations, and "+GetQString(RemoveLabel)+" to remove the selected process before starting."
                        ]
                    },
                    {
                        [CalcResultLabel+" Subpanel"]: [
                           "Available if "+GetQString(FixedPointLabel)+" is selected as the calculation type. Click "+GetQString(MenuLabels.start)+" to start a calculation using current parameters and options, then the results are displayed in this subpanel when it is completed."
                        ]
                    }
                ]
            },
            {
                [sections.preproc]: [
                    "The "+GetQString(sections.preproc)+" tabbed panel assists the pre-processing, or the arrangement of numerical conditions not displayed in the "+GetQString(sections.main)+" panel.",
                    {
                        [sections.dataimp]: [
                            "Import a data set prepared by the user, which is necessary for several types of calculations. The types of data sets available in SPECTRA are summarized below.",
                            "@import",
                            "Meanings of the items and variables are as follows.",
                            [
                                "ListedItem",
                                "time: arrival time, or longitudinal position along the electron bunch",
                                "DE/E: normalized energy deviation (dimensionless)",
                                "I: beam current (A)",
                                "j: beam current density (A/100%)",
                                "z: longitudinal coordinate along the beam axis",
                                "Bx,By: horizontal and vertical magnetic fields",
                                "Gap: gap of the ID",
                                "Depth: depth positions where the Volume Power Density is calculated"
                            ],
                            "The unit of j may need to be explained; it is given as the current per unit energy band; in a mathematical form, \\[I(t)=\\int j\\left(t, \\frac{DE}{E}\\right) d\\frac{DE}{E}\\]",
                            "The format of the ASCII file for the 1D data is as follows (magnetic field distribution as an example)",
                            GetDirectPara("z\tBx\tBy\n-8.959978e-01\t5.174e-05\t7.035e-06\n-8.949972e-01\t5.423e-05\t7.062e-06\n-8.939967e-01\t5.646e-05\t7.244e-06\n\t\t(omitted)\n 8.979989e-01\t4.801e-05\t6.639e-06\n 8.989994e-01\t4.582e-05\t6.327e-06\n 9.000000e-01\t4.409e-05\t6.456e-06\n"),
                            "The 1st line (title) is optional. In the above format, the interval of the independent variable (z) does not have to be necessarily constant, which is not the case for the 2D data; the format should as follows",
                            GetDirectPara("time\tDE/E\tj\n-1.0e-3\t-0.01\t0.001\n-0.9e-3\t-0.01\t0.002\n-0.8e-3\t-0.01\t0.003\n    (omitted)\n0.8e-3\t-0.01\t0.003\n0.9e-3\t-0.01\t0.002\n1.0e-3\t-0.01\t0.001\n-1.0e-3\t-0.008\t0.001\n-0.9e-3\t-0.008\t0.002\n-0.8e-3\t-0.008\t0.003\n    (omitted)\n0.8e-3\t-0.008\t0.003\n0.9e-3\t-0.008\t0.002\n1.0e-3\t-0.008\t0.001\n    (omitted)\n-1.0e-3\t0.01\t0.001\n-0.9e-3\t0.01\t0.002\n-0.8e-3\t0.01\t0.003\n    (omitted)\n0.8e-3\t0.01\t0.003\n0.9e-3\t0.01\t0.002\n1.0e-3\t0.01\t0.001\n"),
                            "For reference, such a data format is created in the C/C++ language as follows.",
                            GetDirectPara("for(n = 0; n < N; n++){\n  for(m = 0; m < M; m++){\n    cout << t[m] << \" \" << de[n] << \" \" <<  j[m][n] << endl;\n  }\n}"),
                            "Note that the order of the \"for loop\" is arbitrary; the 1st and 2nd lines can be swapped in the above example.",
                            "After preparing the ASCII file, click "+GetQString(MenuLabels.import)+" button and specify the file name in the dialog box to import it. The unit of each item should be chosen before importing, in the "+GetLink(EditUnitsLabel, EditUnitsLabel, false)+" dialog box that pops up by running "+GetMenuCommand([MenuLabels.edit, EditUnitsLabel])+" command. Note that the unit of the imported data cannot be changed, so you need to import the data again with the correct unit in case a wrong unit has been chosen. Also note that the units of several items (I, j, DE/E) are fixed, and cannot be selected when importing."
                        ]
                    },
                    {
                        "Visualization": [
                            "After importing, the data sets can be visualized to verify if the configurations (unit and format of the data file) are correct. An example is shown below.",
                            {"type":"figure", "src":"preproc.png", "caption":"Example of the "+GetQString(sections.preproc)+" tabbed panel. The relation between the gap and field amplitude of an undulator is plotted in this example."},
                            "In the left bottom side, the data contents in "+GetLink(sections.json, sections.json, false)+" are shown.",
                            "Besides the imported data sets as described above, there exist a number of items that can be visualized, which are listed in the top left of this subpanel. Just click one of them for visualization. Note that several of them are available only under specific conditions, which are summarized below.",
                            "@preproc",
                            {
                                [sections.phaseerr] : [
                                    "It is well known that the effects due to magnetic errors in undulators can be evaluated using an analytical formula \\[I_r/I_0=\\exp(-k^2\\sigma_{\\phi}^2),\\] where $I_0$ means the photon intensity available with an ideal condition, $I_r$ means that in a real condition with magnetic errors, $k$ is the harmonic number, and $\\sigma_{\\phi}$ is the RMS phase error.", 
                                    "Although the above formula is valid for radiation emitted by a single electron observed on axis (with an infinitely narrow angular acceptance), it overestimates the effects due to magnetic errors in a more realistic condition that the electron beam emittance and energy spread are finite, and/or the the angular acceptance in the beamline is not narrow; these factors effectively work to recover the normalized intensity $I_r/I_0$. To estimate $I_r/I_0$ with these recovery factors, an alternative method "+GetLink("refunivperr", refidx.refunivperr, false)+" can be used, whose results are shown together with those using the conventional method."
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                [sections.postproc]: [
                    "The "+GetQString(sections.postproc)+" tabbed panel assists the user to visualize the calculation results. The output file is automatically loaded upon completion of a calculation, or alternatively, the existing output files can be imported. To do so, click "+GetQString("Import")+" button and specify the location of the output file.",
                    {"type":"figure", "src":"postproc.png", "caption":"Example of the "+sections.postproc+" tabbed panel, showing the energy spectrum of the flux density."},
                    "For visualization, select more than one item from "+GetQString("Items to Plot")+". The dimension of the plot depends on the calculation type of the loaded file. In a 1D plot, a desired area can be zoomed in by dragging. Other options are available to operate the plot, by clicking one of the small icons located in the right top of the plot. For details, refer to the documents about "+GetQString("Plotly")+" library to be found online.",
                    "Besides the above options, the plot can be configured by right-clicking and running one of the context menus: switch the scale (linear or log), change the 2D plot type (contour or surface), or change the method of scaling in each frame for multidimensional plot (see below).",
                    {
                        [sections.compplot]: [
                            "If more than one output file is loaded with the same calculation type, "+GetQString(sections.compplot)+" is available, and possible data names are shown. Click the desired ones to compare the results."
                        ]
                    },
                    {
                        [sections.mdplot]: [
                            "There exist a number of calculation types to generate 3D or 4D output data in SPECTRA (including the "+GetLink(sections.scan, sections.scan, false)+" option), which cannot be plotted in a straightforward manner. In SPECTRA, the 3D/4D data are \"sliced\" into a number of data sets and plotted as a 1D or 2D graph. As an example, let us consider the visualization of a Wigner function calculated in the 4D phase space (X,X',Y,Y'). SPECTRA offers several combinations for plotting and slicing variables. If a pair (X,X') is chosen as the plotting variable, then the data is sliced at each (Y,Y') position, and 2D plot (Brilliance vs X,X') is created. Note that the coordinates of the slicing variables can be arbitrary chosen within the possible range, by dragging the sliders indicating their positions."
                        ]
                    },
                    {
                        [sections.ascii]: [
                            "The visualization result, or the data set(s) currently plotted, can be exported as an ASCII file by clicking "+GetQString(sections.ascii)+" button."
                        ]
                    },
                    {
                        [sections.donwload]: [
                            "Available in the web-application mode. The whole calculation result can be downloaded as an JSON file by clicking "+GetQString(sections.donwload)+" button."
                        ]
                    }
                ]
            },
            {
                [sections.prmset]: [
                    "In SPECTRA, parameters and numerical conditions displayed in the "+GetQString(AccLabel)+", "+GetQString(SrcLabel)+" and "+GetQString(ConfigLabel)+" subpanels are separately saved in JSON objects, each of which is referred to as a "+sections.prmset+". For example, "+GetQString(AccLabel+" "+sections.prmset)+" means a JSON object that stores the parameters displayed in the "+GetQString(AccLabel)+" subpanel. In addition, "+GetQString(BLLabel+" "+sections.prmset)+" is available to bundle the three "+sections.prmset+"s, which represent a \"beamline\" in a specific SR facility. Each "+sections.prmset+" can be switched from one to another by selecting from the submenus in "+GetQString(sections.prmset)+" main menu. Note that each "+sections.prmset+" can be duplicated, renamed, or deleted. To do so, right click the target "+sections.prmset+" and run one of the commands in the context menu."
                ]
            },
            {"Menu Commands": [
                {[MenuLabels.file]:["@filemenu"]},
                {[MenuLabels.calc]:["Select the type of calculation. Refer to "+GetLink(CalcTypeLabel, CalcTypeLabel, false)+" for details."]},
                {[MenuLabels.run]:["@runmenu"]},
                {[sections.prmset]:["Select and edit the "+GetQString(sections.prmset)+", Refer to "+GetLink(sections.prmset, sections.prmset, false)+" for details."]},
                {[MenuLabels.edit]:["Open one of the "+GetLink(sections.setupdlg, sections.setupdlg, false)+" to set up various configurations, not included in the "+sections.prmset+"s."]},
                {[MenuLabels.help]:["Open the reference manual or show the information about SPECTRA."]}
            ]},
            {"Setup Dialogs": [
                "Open a dialog to edit miscellaneous parameters besides those displayed in the main panel. Details of each dialog are explained below.",
                "@setupdlg"
            ]},
            {[sections.plotlyedit]: [
                "Besides standard Plotly.js configurations, a number of options to edit the graphical plot in the Post- and Pre-Processing are available. To do so, click the small icon located in the top-right side of the plot. Then a dialog box pops up to let the user edit the plot in the following configurations.",
                "@plotlyedit"
            ]}
        ]
    },
    {
        [chapters.prmlist]: [
            "All the parameters available in the subpanels of the "+GetQString(sections.main)+" panel are summarized below, for each subpanel.",
            {
                [AccLabel]: [
                    "@accprm",
                    {
                        [AccTypeCaption]: [
                            "In SPECTRA, the accelerators are categorized into two types: "+GetQString("Storage Ring")+" and "+GetQString("Linear Accelerator")+". The difference between them is how to specify the average beam current. In the former, it is directly specified by the user. In the latter, the pulse repetition rate and bunch charge should be given to evaluate the average current."
                        ]
                    }
                ]
            },
            {
                [SrcLabel]: [
                    "@srcprm",
                    {
                        [SrcTypeCaption]: [
                            "Details of the type of the light sources available in SPECTRA are summarized below.",
                            "@srctype"
                        ]
                    }
                ]
            },
            {
                [ConfigLabel]: [
                    "@confprm",
                    {
                        [sections.binary]: [
                            "The binary format to export the modal profile is defined below.",
                            [
                                "ListedItem",
                                "Integer (4 byte) $\\times\\:3$: $N_m$, $N_X$, $N_Y$",
                                "Double (8 byte) $\\times\\:2$: $\\Delta X$, $\\Delta Y$",
                                "Double (8 byte) $\\times\\:N_XN_Y$: 0-th Mode Profile Real Part",
                                "Double (8 byte) $\\times\\:N_XN_Y$: 0-th Mode Profile Imaginary Part",
                                "...",
                                "Double (8 byte)$\\times N_XN_Y$: ($N_m$-1)-th Mode Profile Imaginary Part",
                            ],
                            "where $N_m$ is the number of coherent modes, $\\Delta X$ and $N_{X}$ are the interval and number of positions along the horizontal (X) axis, and similar expressions for the vertical (Y) axis. The order index j in each array representing the real/imaginary part of the complex amplitude is given as \\[j=j_x+j_yN_X\\] where $j_x$ and $j_y$ refer to the order indices corresponding to the X and Y positions. To be specific, the X index changes first.",
                        ]
                    }
                ]
            }
        ]
    },
    {
        [chapters.calcsetup]: [
            "Details of how to setup and start the calculations are presented here, together with explanations of the type of calculations and output items available in SPECTRA.",
            {
                ["General Method"]: [
                    {
                        ["Open a Parameter File"]: [
                            "Upon being started, SPECTRA tries to load parameters from the parameter file that was opened last time. If successful, the parameters are shown in the "+GetQString(sections.main)+" panel. If SPECTRA is run for the first time after installation, default parameters will be shown. To open a new SPECTRA parameter file, run "+GetMenuCommand([MenuLabels.file, MenuLabels.open])+" command. In the initial setting, the parameter files are found in the directory \"[SPECTRA Home]/prm\" with a default suffix \"json\", where \"[SPECTRA Home]\" is the directory in which SPECTRA has been installed."
                        ]
                    },
                    {
                        ["Select a "+CalcTypeLabel]: [
                            "Before starting any calculation, "+GetQString(CalcTypeLabel)+" should be selected by running one of the submenus in "+GetMenuCommand([MenuLabels.calc])+". Refer to "+GetLink(CalcTypeLabel, CalcTypeLabel, false)+" for details of each calculation type."
                        ]
                    },
                    {
                        ["Arrange the Output File"]: [
                            "Arrange the output file to save the calculation results in the "+GetLink(OutFileLabel+" Subpanel", OutFileLabel, false)+" subpanel."
                        ]
                    },
                    {
                        [MenuLabels.start]:[
                            "Run "+GetMenuCommand([MenuLabels.run, MenuLabels.start])+" command to start a single calculation. Then "+GetQString(CalcProcessLabel)+" subpanel is displayed in the "+GetQString(sections.main)+" panel to indicate the progress of calculation. To cancel the calculation, click "+GetQString(CancelLabel)+" button. Note that the serial number is automatically incremented once the calculation is started, unless it is not negative (-1). This is to avoid the overlap of the output file name in performing successive calculations. When the calculation is completed, the "+GetQString(CalcProcessLabel)+" subpanel vanishes and the result is imported in the "+GetQString(sections.postproc)+" panel for visualization."
                        ]
                    },
                    {
                        ["Verify the Result"]: [
                            "Upon completion of a calculation, the output file is automatically loaded and one of the items is plotted in the "+GetQString(sections.postproc)+" subpanel to quickly view the results. Refer to "+GetLink(sections.postproc, sections.postproc, false)+" for details about how to operate the "+sections.postproc+"."
                        ]
                    }
                ]
            },
            {
                [CalcTypeLabel]: [
                    "To start any calculation in SPECTRA, the "+GetQString(CalcTypeLabel)+" should be specified first. This is shown as the submenus of "+GetMenuCommand([MenuLabels.calc])+" main menu in the GUI. The meanings and details of the submenus are summarized in the table below. After selection, the calculation type is shown in the top of the "+GetQString(ConfigLabel)+" subpanel, which is represented by a string given by concatenating a number of submenu items. Note that a \"double colon (::)\" is inserted between items for clarity.",
                    "@calctype",
                ]
            },
            {
                [sections.outitems]: [
                    "The output items specific to respective calculation types are summarized below.",
                    "@outitems"
                ]
            },
            {
                [CalcProcessLabel]: [
                    "To configure a number of calculations with different conditions, run "+GetMenuCommand([MenuLabels.run, "Create Process"])+" command every time you finish specifying all the parameters. Then the "+GetQString(CalcProcessLabel)+" subpanel appears in the "+GetQString(sections.main)+" panel to show the calculation list currently saved in a temporary memory. Repeat it until all the calculations are specified. Click "+GetQString(RemoveLabel)+" button to delete the selected process, or "+GetQString(CancellAllLabel)+" to clear out all the processes. Run "+GetMenuCommand([MenuLabels.run, MenuLabels.start])+" command to start the calculation processes, then a progressbar is displayed to show the status of each process."
                ]
            },
            {
                [sections.scan]: [
                    "Besides the method described above, it is possible to configure a lot of "+CalcProcessLabel+" at once by scanning a specific parameter. To do so, right click the target parameter in one of the subpanels after selecting the "+CalcTypeLabel+", and click "+GetMenuCommand(["Scan This Parameter"])+" in the context menu. Then specify the configurations for scanning in the dialog box as shown below. Note that the context menu does not pop up for parameters that cannot be used for scanning.",
                    {"type":"figure", "src":"scanconfig.png", "caption":"Configuration for scanning a parameter."},
                    "Input the initial & final values, and number of points for scanning. For several parameters to be specified by an integer, scanning interval instead of the number of points should be given. Note that the "+GetQString("Bundle the output data")+" option is to bundle all the output data into a single output file, which can be retrieved later in the "+GetQString(sections.postproc)+" subpanel. The availability of this option depend on the selected "+CalcTypeLabel+".",
                    "If the target parameter forms a pair, such as &beta;<sub>x, y</sub> (horizontal and  betatron functions), the user is requested to select the dimension for scanning: "+GetMenuCommand(["Scan Parameter 1D/2D"])+". For the 2D scanning, configurations for the both parameters are needed.",
                    "After configuration, click "+GetQString("OK")+" button to create a "+GetQString(CalcProcessLabel)+". Then the specified parameters are saved in a temporary memory and the scanning process is saved in the calculation list. Run "+GetMenuCommand([MenuLabels.run, MenuLabels.start])+" command to start the calculation.",
                    {
                        [sections.kxyscan]: [
                            "When scanning the fundamental energy of undulators with both of the horizontal and vertical K values (K<sub>x</sub> and K<sub>y</sub>), such as elliptic undulators, the ratio of the two (K<sub>x</sub>/K<sub>y</sub>) depends on "+GetQString(SrcPrmsLabel.gaplink[0])+" option as summarized below.",
                            "@e1scan"
                        ]
                    }
                ]
            },
            {[sections.ppcomp]: [
                "To reduce the computation time, parallel computing based on the MPI is available in SPECTRA. To enable this option, refer to "+GetLink(EditMPIConfig, EditMPIConfig, false)+" setup dialog."
                ]
            }
        ]
    },
    {
        [chapters.spcalc]: [
            "Besides the fundamental properties of SR such as the flux and radiation power, which can be calculated in a rather straightforward manner, SPECTRA offers a method to evaluate a number of special characteristics of SR: "+MenuLabels.spdens+", "+MenuLabels.vpdens+", "+MenuLabels.srcpoint+", "+MenuLabels.CMD+". In what follows, details of them are explained.",
            {
                [MenuLabels.spdens]: [
                    "The surface power density is defined as the radiation power per unit surface area of the target object, which should be distinguished from the (normal) power density defined as the power per unit area of the transverse (x,y) plane. If the normal vector of the surface of the target object is parallel to z, there is no difference between the two. This is not the case when the normal vector is perpendicular to z; the surface power density in this configuration is much lower than the normal power density as easily understood.",
                    "Computation of the surface power density is usually much more complicated than that of the normal power density. This comes from the fact that the incident angle of SR largely depends on the longitudinal position where it is emitted, if the surface of the target object has a small glancing angle. This is not the case for computing the normal power density, where the incident angle is always nearly 90 degrees."
                ]
            },
            {
                [MenuLabels.vpdens]: [
                    "The volume power density is defined as the radiation power absorbed per unit volume in an object illuminated by radiation. In a mathematical form it is given by \\[\\frac{d^3P(x,y,D)}{dxdydD}=C\\int \\frac{d^2F(x,y,\\omega)}{dxdy}[1-\\mbox{e}^{-\\mu(\\omega)D}]\\mu_{en}(\\omega)d\\omega,\\] where $\\mu$ & $\\mu_{en}$ are the linear attenuation & energy absorption coefficients at the photon energy $\\hbar\\omega$, $D$ is the distance from the surface of the object (\"Depth\"), and $C$ is a unit conversion factor. Note that glancing-incidence conditions can be specified as explained in the <a href=\"#volpdens.png\"> relevant parameters</a>."
                ]
            },
            {
                [MenuLabels.srcpoint]: [
                    "In contrast to other calculations in which the observation point is assumed to be located downstream of the light source, characteristics exactly at the source point (center of the light source, z=0) are evaluated in this calculation. This is possible by propagating the emitted radiation backward to the source point using wave optics. Two options are available as follows.",
                    {
                        [MenuLabels.wigner]:[
                            "The photon flux density in the phase space spanned by the spatial $(x,y)=\\boldsymbol{r}$ and angular $(x',y')=\\boldsymbol{r}'$ coordinates, which is referred to as the phase-space density and denoted by $d(x,y,x',y')$, is an important physical quantity to characterize SR as a light source. Its maximum value, which is known as brilliance or brightness, gives the information of how many coherent photons are available. Its distribution in the phase space is necessary to carry out the ray-trace simulation based on the geometrical optics.", 
                            "It is worth noting that the angular profile of SR in the far-field region is obtained by integrating $d(x,y,x',y')$ over $(x,y)$, while the spatial profile in the near-field region is obtained by integrating over $(x',y')$. Also note that these spatial and angular profiles can be computed directly from an analytical formulas based on classical electrodynamics. It should be noted, however, that there is no analytical method to calculate $d(x,y,x',y')$ directly from the first principle. The Wigner function $W(x,y,x',y')$ is introduced in SR formulation to solve this problem and makes it possible to compute $d(x,y,x',y')$ from the complex amplitude of radiation.",
                            "SPECTRA is equipped with several functions to compute the phase-space density not only for the single electron, but also for more practical conditions, i.e., the electron beam with finite emittance and energy spread. The resultant phase-space density can be computed as a function of various variables: photon energy, K value, and phase-space coordinates. For details of numerical implementation of the Wigner function, refer to "+GetLink("refwigner", refidx.refwigner, false)+".",
                            {
                                [MenuLabels.energy]: [
                                    "The phase-space density is calculated as a function of the photon energy with other conditions being fixed. In the case of undulator radiation, the target harmonic number should be specified as well."
                                ]
                            },
                            {
                                [MenuLabels.Kvalue]: [
                                    "The phase-space density of undulator radiation at a specific harmonic is calculated as a function of the undulator K value. Note that the photon energy should be given as a detuning parameter with respect to the exact harmonic energy. If the calculation is done on-axis (x=y=x'=y'=0), the resultant data are comparable to the brilliance roughly estimated by a Gaussian approximation, but are based on a more rigorous method using the Wigner function."
                                ]
                            },
                            {
                                [MenuLabels.phasespace]: [
                                    "The distribution of the phase-space density is calculated as a function of the phase-space coordinate variables: x, y, x', and y'. Five types of calculation conditions are available as follows.",
                                    [
                                        "NumberedItem",
                                        "X-X' (Sliced): $W(x,y_{fix},x',y_{fix}')$",
                                        "X-X' (Projected): $W_x(x,x')$",
                                        "Y-Y' (Sliced): $W(x_{fix},y,x_{fix}',y')$",
                                        "Y-Y' (Projected): $W_y(y,y')$",
                                        "X-X-Y-Y' : $W(x,y,x',y')$"
                                    ],
                                    "where $W_x$ is defined as \\[W_x=\\int\\!\\!\\!\\!\\int W(x,x',y,y')dydy',\\] and a similar expression for $W_y$."
                                ]
                            },
                            {
                                [MenuLabels.Wrel]: [
                                    "When the 4D phase-space density is calculated, two important properties related to the Wigner function method are available: separability and total degree of spatial coherence. The details of them are explained as follows.",
                                    "@wigrel",
                                    "Note that the above properties, $\\kappa$, $\\zeta$, $\\zeta_x$, and $\\zeta_y$ are evaluated by a simple summation of quadratic forms of Wigner functions given at a number of grid points specified by the user, and the accuracy of integration is not checked. The user is required to input the range and number of mesh that are sufficiently wide and large to obtain a reliable result. One solution is to first check the profile of the projected Wigner functions in the 2D phase space, then input these parameters."
                                ]
                            }
                        ]
                    },
                    {
                        [MenuLabels.sprof]:[
                            "Spatial profile of the photon density, i.e., the spatial flux density is computed at the source point. This may be useful when discussing the profile of the photon beam after focusing optical components in the SR beamline. To be more specific, the spatial profile computed with this scheme reproduces the photon beam profile at the focal point of the unit magnification optical system."
                        ]
                    }            
                ]
            },
            {
                [MenuLabels.CMD]: [
                    MenuLabels.CMD+" is a mathematical method to decompose the partially coherent radiation into a number of coherent modes. Because the propagation of each mode can be described by wave optics, designing the optical elements can be much more reliable than that with the conventional ray-tracing that is based on geometrical optics.",
                    {
                        ["Mathematical Form"]: [
                            "In the numerical CMD implemented in SPECTRA, the Wigner function $W$ is supposed to be approximated by $W'$ composed of several coherent modes, namely, \\[W'=f\\sum_{p=0}^{M}\\mathscr{W}(\\Psi_p,\\Psi_p),\\] with $\\mathscr{W}$ meaning an operator to calculate the Wigner function of the $p$-th order coherent mode, whose complex amplitude is represented by a function $\\Psi_p$, and $M$ is the maximum order of the coherent modes. The function $\\Psi_p$ is assumed top have a form \\[\\Psi_p=\\sum_{q=0}^{N_p}a_{h,j}\\phi_h(\\hat{x})\\phi_j(\\hat{y}),\\] with \\[\\phi_m(\\zeta)=\\frac{2^{1/4}}{\\sqrt{2^m m!}}\\mbox{e}^{-\\pi\\zeta^2}H_m(\\sqrt{2\\pi}\\zeta),\\] denoting the m-th order Hermite-Gaussian (HG) function, where $\\hat{\\boldsymbol{r}=(\\hat{x},\\hat{y})=(x/\\sqrt{\\pi}w_x,y/\\sqrt{\\pi}w_y)}$ is the normalized transverse coordinate, $a_{h,j}$ is the amplitude of the HG function of $\\phi_h(\\hat{x})\\phi_j(\\hat{y})$, $H_m$ is the Hermite polynomial of the order $m$, and $N_p$ denotes the maximum order of the HG modes in the p-th coherent mode. Note that the indices $h$ and $j$ are given as a function of the integer $q$ and order $p$. The coefficient $f$ and the dimension of $a_{h,j}$ are chosen arbitrarily as long as the above formulas are satisfied. In SPECTRA, they are determined so that $a_{h,j}$ is dimensionless, and \\[\\sum_{p=0}^{\\infty}\\int|\\Psi_p|^2d\\hat{\\boldsymbol{r}}=1\\] is satisfied. The purpose of the numerical CMD is to compute the coefficient $a_{h,j}$ so that the resultant Wigner function $W'$ well reproduces the original function $W$. For details of the CMD method in SPECTRA, refer to "+GetLink("refcmd", refidx.refcmd, false)+"."
                        ]
                    },
                    {
                        ["How to Do?"]: [
                            "To perform the CMD in SPECTRA, follow the steps explained below.",
                            [
                                "ListedItem",
                                "Preparation of the Wigner Function: Before starting the CMD, the user should compute the Wigner function in the phase space. In addition to the 4D Wigner function $W(x,y,x',y')$, the projected ones ($W_x$ and $W_y$), are also available, in which case 1D modal functions are given in the respective direction (horizontal or vertical). The range and number of points to calculate the Wigner function should be reasonably wide and large. Note that the JSON format should be chosen as the format of the "+GetLink(OutFileLabel+" Subpanel", "output file", false)+".",
                                "Load the Wigner Function: Open the JSON output file storing the Winger function data generated in the above step, by running [File]-[Open a Parameter File] command. If the Wigner function data is successfully loaded, [CMD with the Wigner Function] menu is enabled under the [Select Calculation]-[Coherent Mode Decomposition] menu. Run it to show configurations for the CMD.",
                                "Arrange the Parameters: In the "+ConfigLabel+" subpanel, edit the parameters and options related to the CMD; refer to "+GetLink(CMDParameterLabel, CMDParameterLabel, false)+" for details. After configuration, run [Run]-[Start Calculation] command to start the CMD process.",
                                "Verify the Result: The results of the CMD, such as the modal amplitude $a_{h,j}$, maximum orders of the HG functions, and numerical errors in the CMD process, are save in the output file, which can be directly verified by opening the output file in any text editor.",
                                "Visualization: other data sets specified in the options before starting the CMD, such as the modal profiles and reconstructed Wigner functions, are save as well, which can be visualized in the "+GetQString(sections.postproc)+" panel."
                            ]
                        ]
                    }
                ]
            }
        ]
    },
    {
        [chapters.format]: [
            "Besides the operation based on the GUI, SPECTRA (more precisely, the solver) can be utilized to communicate with external codes for the so-called start-to-end simulations. This actually requires the knowledge of the format of the input and output files, which is explained in the followings.",
            {
                [sections.json]: [
                    "To deal with the many parameters and options, SPECTRA utilizes the JSON (JavaScript Object Notation) format, which is described by a number of \"objects\". The object contains a number of \"pairs\" formed by a \"key\" and \"value\", separated by a colon \":\", and should be enclosed by a curly bracket {}. The value can be one of the followings: number, array, string and (another) object. An example of the SPECTRA input file is as follows.",
                    GetDirectPara("{\n  \"Accelerator\": {\n    \"Energy (GeV)\": 8,\n    \"Current (mA)\": 100,\n    ....\n    \"Options\": {\n      \"Zero Emittance\": false,\n      \"Zero Energy Spread\": false\n    }\n  },\n  \"Light Source\": {\n    \"B (T)\": 0.33467954834861074,\n    \"&lambda;<sub>u</sub> (mm)\": 32,\n    ....\n  },\n  \"Configurations\": {\n    \"Distance from the Source (m)\": 30,\n    ....\n  },\n  \"Output File\": {\n    \"Comment\": \"\",\n    ....\n  }\n}"),
                    "In this example, four JSON objects are found, whose keys are "+GetQString(AccLabel)+", "+GetQString(SrcLabel)+", "+GetQString(ConfigLabel)+", and "+GetQString(OutFileLabel)+". The value of each object is also an object, which actually specifies the parameters and options, such as \"Energy (GeV)\": 8, denoting the energy of the electron beam to be 8 GeV.",
                    "For details of the JSON format, please refer to any document available online or found in the text."
                ]
            },
            {
                [sections.input]: [
                    "The input file to be loaded by the solver should have 4 JSON objects: "+GetQString(AccLabel)+", "+GetQString(SrcLabel)+", "+GetQString(ConfigLabel)+", and"+GetQString(OutFileLabel)+". Details of each object are summarized below, where \"GUI Notation\" is the parameter name displayed in the "+GetQString(MenuLabels.main)+" GUI panel, \"Key\" is the name of the key to be used in the input file, \"Format\" is the format of the value, and \"Default\" is the default value. Note that the key name can be either of the \"Full\" or \"Simplified\" expression.",
                    {
                        [AccLabel+" Object"]: [
                            "@accjson"
                        ]    
                    },
                    {
                        [SrcLabel+" Object"]: [
                            "@srcjson"
                        ]    
                    },
                    {
                        [ConfigLabel+" Object"]: [
                            "@confjson"
                        ]    
                    },
                    {
                        [OutFileLabel+" Object"]: [
                            "@outjson"
                        ]    
                    }
                ]
            },

            {
                [sections.output]: [
                    "If \"JSON\" or \"Both\" is chosen as the \"Format\" option in the "+GetLink(OutFileLabel+" Subpanel", OutFileLabel)+" subpanel, a JSON format output file is generated after the calculation completes. Besides the visualization in the "+GetQString(sections.postproc)+" panel, it can be used for further processing with other external codes. To facilitate it, the structure of the output file is explained below. Note that the order index (for example of an array, column, etc.) in the followings is defined as starting from \"0\", but not from \"1\".",
                    {
                        [GetQString("Input")+" Object"]: ["All the parameters and options are stored in this object with the same format as the "+GetLink(sections.input, sections.input, false)+". If the output file is opened in the GUI (as an input parameter file), these parameters are displayed and can be used again."]
                    },
                    {
                        [GetQString("Output")+" Object"]: [
                            "The calculation results are stored in this object.",
                            "@outdata",
                            "The format of the \"data\" object (2D array) is as follows.",
                            [
                                "ListedItem",
                                "0th ~ (n-1)-th array: independent variables, where n is the dimension. The length of each array corresponds to the number of calculation points. For example, it is defined by \"Points (Energy)\" parameter for \"Energy Dependence\" calculations.",
                                "n-th ~ (n+m-1)-th array: calculated items, where m is the number of items. The length of each array corresponds to the product of the lengths of the independent variable arrays."
                            ],
                            "As an example, let us consider an \"Output\" object as follows",
                            GetDirectPara("\"Output\": {\n    \"dimension\": 1,\n    \"titles\": [\"Energy\",\"Flux Density\",\"GA. Brilliance\",\"PL(s1/s0)\",\"PC(s3/s0)\",\"PL45(s2/s0)\"],\n    \"units\": [\"eV\",\"ph/s/mr^2/0.1%B.W.\",\"ph/s/mm^2/mr^2/0.1%B.W.\",\"\",\"\",\"\"],\n    \"data\": [\n      [5000,5005,...,49995,50000],\n      [4.02638e+14,3.98914e+14,...,6.66718e+16,6.81642e+16],\n      [3.2776e+16,3.24789e+16,...,6.64598e+18,6.79476e+18],\n      [0.999949,0.999947,...,0.999703,0.999713],\n      [0,0,...,0,0],\n      [-8.67036e-18,-8.97758e-18,...,-1.72714e-17,-1.6893e-17]\n    ]\n  }"),
                            "The data is composed of 1 independent variable (Energy) and 5 items (Flux Density etc.). The 0th array ([5000,...]) corresponds to the photon energy, and the 1st ([4.02638e+14,...]) to the flux density, etc.",
                            "In case the dimension is larger than 1 and thus more than one independent variables exist, the order index j of the item array is given as \\[j=j_0+j_1N_0+j_2N_0N_1+\\cdots,\\] where $j_i$ and $N_i$ refer to the order index and number of data points of the $i$-th variable.",
                            "In some case, 3D data array composed of a number of 2D arrays with the same format as above is stored; each of 2D array is characterized by the \"details\" object. An example is shown below.",
                            GetDirectPara("  \"Output\": {\n    \"dimension\": 1,\n    \"titles\": [\"Harmonic Energy\",\"Peak Energy\",\"K Value\",\"Gap\",\"Flux Density\",...],\n    \"units\": [\"eV\",\"eV\",\"\",\"\",\"ph/s/mr^2/0.1%B.W.\",...],\n    \"details\": [\"Harmonic: 1\",\"Harmonic: 3\",\"Harmonic: 5\"],\n    \"data\": [\n      [\n        [18977.5,18707.1,...,4702.57,4336.24],\n        [18927.2,18657.6,...,4692.37,4326.97],\n        [0.040015,0.174748,...,2.46527,2.6],\n        [50,35.2675,...,8.58047,8.01609],\n        [7.24659e+15,1.3423e+17,...,1.90452e+18,1.82972e+18],\n        [6.91663e+17,1.27995e+19,...,1.5325e+20,1.44896e+20],\n        [0.999995,0.999995,...,0.999998,0.999998],\n        [0,0,...,0,0],\n        [-6.23832e-19,-6.15261e-19,...,-8.10339e-19,-7.90166e-19]\n      ],\n      [\n        [56932.5,56121.2,54374,...,14107.7,13008.7],\n        [47488.9,56019.4,54276.1,...,15312,14087.7,12990.4],\n        [0.040015,0.174748,...,2.46527,2.6],\n        [50,35.2675,...,8.58047,8.01609],\n        [3.235e+10,5.91631e+13,...,1.21888e+18,1.20334e+18],\n        .....\n      ],\n      [\n        [94887.4,93535.3,...,23512.9,21681.2],\n        [85444.8,84227.3,...,23487.4,21658],\n        [0.040015,0.174748,...,2.46527,2.6],\n        [50,35.2675,...,8.58047,8.01609],\n        [7.1207e+11,1.37382e+13,...,7.22944e+19,7.31154e+19],\n        .....\n      ]\n    ]\n  }"),
                            "The \"details\" object in this example specify the harmonic number, i.e., 1st, 3rd and 5th harmonics, and the maximum flux density near the harmonic energy, and other related characteristics are calculated as a function of the K value, for the three different harmonic numbers. The \"data\" object is then composed of three 2D arrays and thus forms a 3D array."
                        ]
                    },
                    {
                        ["Objects Related to CMD"]: [
                            "The results of "+GetLink(MenuLabels.CMD, MenuLabels.CMD, false)+", such as the modal amplitude and profiles, are saved separately from the \"data\" object described above. The details of them are explained below.",
                            {
                                [GetQString(MenuLabels.CMD)+" Object"]: [
                                    "@cmdresult",
                                    {
                                        ["How to retrieve the flux and Wigner function from the modal amplitue?"]: [
                                            "The flux density ($I_n$) and Wigner function ($W_n$) of the $n$-th mode can be retrieved form the complex amplitude $a_n$ determined by the CMD according to the following formulas, using the symbols summarized in the above table.",
                                            "For 1D case (CMD with 2D Wigner function):\\[I_n(x)=|a_n(x)|^2\\frac{F}{2\\sqrt{\\pi}\\sigma}\\times 10^{-3},\\] \\[W_n(x,\\theta_x')=\\frac{W_0}{2\\sqrt{\\pi}\\sigma}\\int a_n\\left(x-\\frac{x'}{2}\\right)a_n^*\\left(x+\\frac{x'}{2}\\right)\\mbox{e}^{ik\\theta_x x'}dx',\\]",
                                            "For 2D case (CMD with 4D Wigner function):\\[I_n(\\boldsymbol{r})=|a_n(\\boldsymbol{r})|^2\\frac{F}{4\\pi\\sigma_x\\sigma_y}\\times 10^{-6},\\] \\[W_n(\\boldsymbol{r},\\boldsymbol{\\theta})=\\frac{W_0}{4\\pi\\sigma_x\\sigma_y}\\int a_n\\left(\\boldsymbol{r}-\\frac{\\boldsymbol{r}'}{2}\\right)a_n^*\\left(\\boldsymbol{r}+\\frac{\\boldsymbol{r}'}{2}\\right)\\mbox{e}^{ik\\boldsymbol{\\theta}\\boldsymbol{r}'}d\\boldsymbol{r}',\\]",
                                            "where $k=2\\pi/\\lambda$ is the wavenumber of radiation." 
                                        ]
                                    }
                                ]
                            },
                            {
                                ["Other Objects"]: [
                                    "A number of data sets evaluated by post-processing the CMD results described above are saved as follows. Note that the format of each object is the same as that of the \"data\" object.",
                                    "@cmdpp"
                                ]
                            }
                        ]
                    },
                    {
                        ["Objects Related to FEL Mode"]: [
                            "When "+GetLink(ConfigOptionsLabel.fel[0], ConfigOptionsLabel.fel[0], false)+" and "+GetLink(ConfigOptionsLabel.exportInt[0], ConfigOptionsLabel.exportInt[0], false)+" options are enabled, numerical data generated while solving the FEL equation, such as variation of the electron beam temporal profile and growth of the FEL radiation pulse, are recorded as summarized below.",
                            "@felvar"
                        ]
                    }
                ]
            }
        ]
    },
    {
        [chapters.spusage]: [
            "Besides the standalone desktop application as described above, SPECTRA offers a number of methods to perform calculations, which are described below. Note that in the followings, [spectra_home] refers to the directory where SPECTRA has been installed.",
            {
                ["Run Solver in a Standalone Mode"]: [
                    "When "+GetMenuCommand([MenuLabels.run, MenuLabels.start])+" command is executed, the SPECTRA GUI creates an input parameter file (\"*.json\") and invokes the solver (\"spectra_solver\" or \"spectra_solver_nompi\" depending on whether the parallel computing option is enabled or not) located in the same directory as the main GUI program, with the input file as an argument. This means that SPECTRA (solver) can be run without the GUI, if the input file is prepared by an alternative method, and a batch process will be possible. To do so, prepare the input file according to the descriptions in "+GetLink(sections.input, sections.input, false)+" and run the solver as follows",
                    GetDirectPara("[spectra_home]/spectra_solver_nompi -f [input file]"),
                    "without parallel computing, or",
                    GetDirectPara("mpiexec -n 4 [spectra_home]/spectra_solver_nompi -f [input file]"),
                    "with parallel computing (4 processes in this example).",
                    "It should be noted that the names of the parameters and options (\"key\" of the object) should be totally correct, including the units and inserted space characters. In addition, the number of parameters and options actually needed for a specific calculation depend on its condition. To avoid possible errors and complexity in preparing the input file, it is recommended to create a \"master input file\" specific to the desired calculation type, by running "+GetMenuCommand([MenuLabels.run, MenuLabels.ascii])+". Then, just modify the values of desired parameters to prepare the input file.",
                    "Note that this usage has not been officially supported before ver. 11.0, simply because the input file format was original and difficult to read." 
                ]
            },
            {
                "Call from a Python Script": [
                    "SPECTRA offers a python library (located in [spectra_home]\python directory) so that the functions in the solver can be called from a python script. To do so, import \"spectra\" module and create an instance of \"Solver\" class with an argument (string) to represent the input parameters and options, which can be generated by encoding the dictionary object. Typical usage is as follows.",
                    GetDirectPara("import spectra\nimport json\n\nf = open(\"test.json\")\nprm = json.load(f)\nprm[\"Accelerator\"][\"Energy (GeV)\"] = 6\nprmstr = json.dumps(prm)\nsolver = spectra.Solver(prmstr)\n...\n"),
                    "In this example, the parameters and options saved in the \"test.json\" file are loaded (open), decoded to create a dictionary object \"prm\" (json.load), the electron energy is changed to 6 (GeV), and the \"prm\" object is encoded to generate a string argument \"prmstr\" (json.dumps) to create the instance of Solver class (spectra.Solver). Then, functions of the Solver class can be called. The supported functions are summarized below.",
                    "@python",
                    "A number of python source files and SPECTRA input files to demonstrate the usage are placed in the same directory ([spectra_home]\python). Note that the library file is compiled with python 3.8, and calling from other versions may fail. Also note that "+GetQString("plotly")+" library should be installed to visualize the calculation results."
                ]
            },
            {
                [sections.webapp]: [
                    "Since the core libraries in SPECTRA are based on the web technologies (node.js and javascript), it can be run as a web application. As an example, the web server hosting the SPECTRA home page is running SPECTRA in the web-application mode, so that the user can try it.",
                    "To run SPECTRA as a web application, follow the steps below.",
                    [
                        "NumberedItem",
                        "Install node.js in your computer.",
                        "Download "+GetQString("spectra_web.zip")+" (common to all platforms) from the SPECTRA home page and uncompress it. A number of files and directories are contained in a directory [spectra_web].",
                        "In the [spectra_web] directory, run "+GetQString("npm install")+" to install node modules that are necessary to run SPECTRA as a web application.",
                        "Copy the solver "+GetQString("[spectra_home]/spectra_solver_nompi(.exe)")+"and the parameter file converter "+GetQString("[spectra_home]/conv_spectra(.exe)")+" (optional) to the [spectra_web] directory.",
                        "Before starting, you may need to change the configuration of the web application in terms of the protocol and port, which is done by editing the JSON file "+GetQString("[spectra_web]/web_app.json")+" with the format as follows."+GetDirectPara("{\n    \"protocol\": \"http\",\n    \"ssl\": {\n        \"key\": \"/etc/letsencrypt/live/your.host.name/privkey.pem\",\n        \"cert\": \"/etc/letsencrypt/live/your.host.name/fullchain.pem\"\n    },\n    \"port\": 3000\n}")+"The value of the \"protocol\" key should be either of \"http\" or \"https\", while that of the \"port\" specifies the port number for communication. In the above example, the \"ssl\" object is not actually needed because \"http\" is chosen. If \"https\" is chosen, the computer should be SSL-certificated and relevant files should be given as in the above example (certification is supposed to be made by \"Let's Encrypt\").",
                        "Now in the [spectra_web] directory, run \"node apps.js\" command, and access the URL \"http(s)://hostname:port\" with a web browser, where \"hostname\" is the host name (or \"localhost\" from the same computer) or IP address of the computer.",
                    ]
                ]
            }
        ]
    },
    {
        [chapters.ref]: [
            "@reference"
        ]
    },
    {
        [chapters.ack]: [
            "This software includes the work that is distributed in the Apache License 2.0, and relies on a number of libraries & database as summarized below, which are gratefully appreciated.",
            [
                "ListedItem",
                "Node.js: Javascript runtime environment to run Javascript code without a web browser (https://nodejs.org/en/).",
                "tauri: application toolkit to build software for all major desktop operating systems using web technologies. (https://tauri.app/)",
                "Plotly.js: Javascript graphing library to facilitate data visualization (https://nodejs.org/en/)",
                "Boost C++: Set of libraries for the C++ language (https://www.boost.org/)",
                "EIGEN: C++ template library for linear algebra (https://eigen.tuxfamily.org/index.php?title=Main_Page)",
                "pybind11: Header-only library to interface C++ and Python languages (https://github.com/pybind/pybind11)",
                "mathjax: Javascript library to display mathematical formulas in HTML documents (https://www.mathjax.org/)",
                "picojson: JSON parser for C++ language (https://github.com/kazuho/picojson)",
                "mucal.c: Source code to calculate the x-ray absorption coefficients (http://www.csrri.iit.edu/mucal.html)",
                "NIST database: Database for the mass energy-absorption coefficients (https://www.nist.gov/pml/x-ray-mass-attenuation-coefficients)"
            ]
        ]
    }
];

//------ create each component
function GetPreprocDetailTable()
{
    let cell, rows = [];
    let table = document.createElement("table");
    let caption = document.createElement("caption");
    caption.innerHTML = "List of items available for visualization";
    table.caption = caption;

    rows.push(table.insertRow(-1)); 
    let titles = ["Name in "+sections.preproc+" Subpanel", "Details", "Availability"];
    for(let j = 0; j < titles.length; j++){
        cell = rows[rows.length-1].insertCell(-1);
        cell.innerHTML = titles[j];    
        cell.className = " title";
        if(j == 0){
            cell.setAttribute("colspan", "2");
        }
    }

    let details ={};
    details[AccLabel] = {
        [PPBetaLabel]: "betatron functions within the light source"
    };
    details[SrcLabel] = {
        [PPFDlabel]: "Magnetic field distribution along the longitudinal axis",
        [PP1stIntLabel]: "1st integrals, corresponding to the velocity of an electron",
        [PP2ndIntLabel]: "2nd integrals, corresponding to the electron trajectory",
        [PPPhaseErrLabel]: "Phase error "+GetLink("refperr", refidx.refperr, false)+" evaluated as a function the magnet pole number. Note that the number of end poles (used for the orbit adjustment and should be eliminated for the phase error evaluation) is automatically determined; to be specific, those with the peak field less than 95% of the average are ignored.",
        [PPRedFlux]: "Reduction of photon intensity at each harmonic due to magnetic errors evaluated by analytical methods. Refer to "+GetLink(sections.phaseerr, "below", false)+" for details."
    };
    details[PPFilters] = {
        [PPTransLabel]: "Transmission rate of the filter",
        [PPAbsLabel]: "Absorption rate of the absorber"
    };
    let remarks ={};
    remarks[AccLabel] = {
        [PPBetaLabel]: ""
    };
    remarks[SrcLabel] = {
        [PPFDlabel]: "",
        [PP1stIntLabel]: "",
        [PP2ndIntLabel]: "",
        [PPPhaseErrLabel]: ["\""+CUSTOM_Label+"\" sources and/or \""+SrcPrmsLabel.phaseerr[0]+"\" option", "2"]
    };
    remarks[PPFilters] = {
        [PPTransLabel]: "\""+ConfigOptionsLabel.filter[0]+"\" options excluding \""+NoneLabel+"\"",
        [PPAbsLabel]: "\""+MenuLabels.vpdens+"\" calculations"
    };
    
    for(let i = 0; i < PreProcessLabel.length; i++){
        let categ = Object.keys(PreProcessLabel[i])[0];
        let values = Object.values(PreProcessLabel[i])[0];
        for(let j = 0; j < values.length; j++){
            rows.push(table.insertRow(-1));
            if(j == 0){
                cell = rows[rows.length-1].insertCell(-1);
                cell.innerHTML = categ;
                if(values.length > 1){
                    cell.setAttribute("rowspan", values.length.toString());
                }
            }

            cell = rows[rows.length-1].insertCell(-1);
            cell.innerHTML = values[j];
    
            cell = rows[rows.length-1].insertCell(-1);
            cell.innerHTML = details[categ][values[j]];

            if(remarks[categ].hasOwnProperty(values[j])){
                cell = rows[rows.length-1].insertCell(-1);
                if(Array.isArray(remarks[categ][values[j]])){
                    cell.innerHTML = remarks[categ][values[j]][0];
                    cell.setAttribute("rowspan", remarks[categ][values[j]][1]);
                }
                else{
                    cell.innerHTML = remarks[categ][values[j]];    
                }
            }
        }
    }
    let retstr = table.outerHTML;

    return retstr;
}

function GetImportDetailTable()
{
    let cell, rows = [];
    let table = document.createElement("table");
    let caption = document.createElement("caption");
    caption.innerHTML = "Data types that can be imported in the "+sections.preproc+" subpanel";
    table.caption = caption;

    rows.push(table.insertRow(-1)); 
    let titles = ["Name in "+sections.preproc+" Subpanel", "Details", "Dimension", "Independent Variable(s)", "Items"];
    for(let j = 0; j < titles.length; j++){
        cell = rows[rows.length-1].insertCell(-1);
        cell.innerHTML = titles[j];    
        cell.className = " title";
    }

    let details = {};
    details[CustomCurrent] = "Current profile of the electron bunch to be used for coherent radiation calculation";
    details[CustomEt] = "Electron density in the (E-t) phase space";
    details[CustomField] = "Magnetic field distribution for "+CUSTOM_Label+" light source";

    details[CustomPeriod] = "Magnetic field distribution within a single period for "+CUSTOM_PERIODIC_Label+" light source";
    details[ImportGapField] = "Relation between the gap and peak field of the ID";

    details[CustomFilter] = "Transmission rate of a filter given as a function of the photon energy";
    details[CustomDepth] = "Depth positions to compute the "+MenuLabels.vpdens;
    details[SeedSpectrum] = "Spectrum of the seed pulse";       
    
    let labels = Object.keys(details);
    for(let i = 0; i < labels.length; i++){
        rows.push(table.insertRow(-1));
        cell = rows[rows.length-1].insertCell(-1);
        cell.innerHTML = labels[i];

        cell = rows[rows.length-1].insertCell(-1);
        cell.innerHTML = details[i];

        let dim = AsciiFormats[labels[i]].dim;
        cell = rows[rows.length-1].insertCell(-1);
        cell.innerHTML = dim.toString();

        let titles = AsciiFormats[labels[i]].titles;
        let tdef = [];
        for(let j = 0; j < dim; j++){
            let idx = titles[j].indexOf("(");
            if(idx < 0){
                tdef.push(titles[j]);
            }
            else{
                tdef.push(titles[j].substring(0, idx));
            }
        }
        cell = rows[rows.length-1].insertCell(-1);
        if(tdef.length > 0){
            cell.innerHTML = tdef.join(", ");
        }

        tdef = [];
        for(let j = dim; j < titles.length; j++){
            let idx = titles[j].indexOf("(");
            if(idx < 0){
                tdef.push(titles[j]);
            }
            else{
                tdef.push(titles[j].substring(0, idx));
            }
        }
        cell = rows[rows.length-1].insertCell(-1);
        cell.innerHTML = tdef.join(", ");
    }
    let retstr = table.outerHTML;
    return retstr;
}

function GetSPECTRAMenuTable(ispython)
{
    let schemes = [
        {far: "Assumes that $|\\boldsymbol{R}|$ is much larger than $|\\boldsymbol{r}|$, where $\\boldsymbol{R}$ and $\\boldsymbol{r}$ represent the vectors directing from the origin to the observer and moving electron, respectively. This implies that the observation angle, i.e., an angle formed by $\\boldsymbol{R}$ and $\\boldsymbol{r}$, is kept constant while the electron passes through the SR source. In addition, the field distribution of the SR source is assumed to be ideal: perfectly periodic in undulators and wigglers, and constant in bending magnets. This significantly simplifies the expressions on SR and thus enables a fast computation. For most applications, such as evaluation of the photon flux passing through a slit and heat load on optical elements, this method is recommended and is in fact reliable enough."},
        {near: "No approximation is made in this method besides an assumption that the electron is relativistic. In other words, the observation angle is a function of the electron position, i.e., it varies while the electron travels along the SR source axis. If the distance between the SR source and observer is shorter and or comparable to the length of the SR source itself, the near-field effect would not be negligible. Especially, the off-axis spectrum will be considerably different from that observed at the point infinitely far from the SR source. In addition, this method should be chosen if the SR source is not ideal. One important case is to compute the characteristics expected in a real device based on a magnetic field distribution actually measured."},
        {cohrad: "Same as \""+MenuLabels.near+"\", except that the radiation is temporally coherent. In other words, radiation emitted by each electron in the electron beam is summed up coherently. This is in contrast to the two methods described above, where radiation is summed up incoherently. The intensity of coherent radiation is significantly enhanced if the bunch length of the electron beam is shorter than the wavelength of radiation, or it has a local density modulation with the typical length shorter than the wavelength."},
        {srcpoint: "Evaluates the photon distribution exactly at the source point, or the center of the SR source. This means that the distance from the source to the observer is zero, i.e., $\\boldsymbol{R}=\\boldsymbol{0}$. Computing the SR properties under such a condition is not possible in a straightforward manner, but requires another numerical operation to propagate the radiation from the observation point back to the source point. SPECTRA is equipped with a number of numerical methods to enable this function."},
        {fixed: "Calculation is performed for a single fixed condition (photon energy, observation point, etc.) and the results are displayed in the GUI."},
        {CMD: "Using the photon distribution at the source point (Wigner functions), partially-coherent radiation can be decomposed into a number of coherent modes, which is useful to describe the propagation of SR in the framework of wave optics."}
    ];
    let methods = [
        {energy: "Target items are calculated as a function of the photon energy."},
        {spatial: "Target items are calculated as a function of the observation point."},
        {Kvalue: "Target items are calculated as a function of the undulator K value (deflection parameter)."},
        {temporal: "Target items are calculated as a function of time."},
        {wigner: "Photon density in the 2D/4D phase space is evaluated by means of the Wigner function method."}
    ];
    let targets = [
        {fdensa: "Photon flux per unit solid angle."},
        {fdenss: "Photon flux per unit area."}, 
        {pflux: "Photon flux of radiation passing through a finite aperture."}, 
        {tflux: "Photon flux of radiation integrated over the whole solid angle."}, 
        SimpleLabel,
        {pdensa: "Radiation power per unit solid angle."}, 
        {pdenss: "Radiation power per unit area."}, 
        {ppower: "Radiation Power passing through a finite aperture"},
        {pdensr: "Radiation power decomposed into polarization and harmonic components"}, 
        {spdens: "Radiation power density under a glancing-incidence condition"}, 
        {vpdens: "Radiation power per unit volume absorbed by a target object (absorber)"}, 
        SimpleLabel,
        {efield: "Temporal profile of electric field of radiation."}, 
        {camp: "Spatial profile of complex amplitude of radiation."}, 
        SimpleLabel,
        {sprof: "Transverse profile of the spatial flux density calculated at the source point."}, 
        {phasespace: "Distribution of the photon density in the in the 2D/4D phase space."}, 
        SimpleLabel,
        {CMD2d: "Perform CMD using the existing Wigner function data"}, 
        {CMDPP: "Perform post-processing using the CMD results"}
    ];
    let conds = [
        {slitrect: "Radiation passes through a rectangular aperture."},
        {slitcirc: "Radiation passes through a circular aperture."},
        SimpleLabel,
        {along: "Moves the observation point along the x- and y-axes."},
        {meshxy: "Moves the observation point over the rectangular grid."},
        {meshrphi: "Moves the observation point over the grid in the 2D polar coordinate."},
        {simpcalc: "Assumes that the radiation is a Gaussian beam, and roughly estimates its characteristics, such as the brilliance, on-axis flux density, source size and angular divergence without actually doing the convolution."},
        SimpleLabel,
        {fluxfix: "Calculates the characteristics of UR at a fixed photon energy. To be specific, the monochromator is unchanged, while the K value is tuned."},
        {fluxpeak: "Calculates the characteristics of UR at peak harmonic energies. To be specific, the monochromator is scanned synchronously with the K value."},
        {powercv: "Calculate the radiation power as a function of the K value."}, 
        SimpleLabel,
        {xzplane: "Calculation is done on the x-z surface located vertically off the beam axis."},
        {yzplane: "Calculation is done on the y-z surface located horizontally off the beam axis."},
        {pipe: "Calculation is done on the inner surface of a pipe coaxially located with the beam axis."},
        SimpleLabel,
        {XXpslice: "4D Wigner function calculated on (X,X') phase space at given (Y,Y')."},
        {XXpprj: "2D (projected) Wigner function calculated on (X,X') phase space."},
        {YYpslice: "4D Wigner function calculated on (Y,Y') phase space at given (X,X')."},
        {YYpprj: "2D (projected) Wigner function calculated on (Y,Y') phase space."},
        {XXpYYp: "4D Wigner function calculated on (X,X',Y,Y')."}
    ];
    let subconds = [
        {tgtharm: "Calculation is performed for individual harmonics."},
        {allharm: "Optimizes the harmonic number to maximize the target item (brilliance or flux)."},
        {Wslice: "4D (X,X',Y,Y') Wigner function at a single point."},
        {WprjX: "2D Wigner function projected on (X,X')."},
        {WprjY: "2D Wigner function projected on (Y,Y')."},
        {Wrel: "Degree of Coherence and X-Y Separability evaluated from Wigner function."}
    ];

    let categories = [
        [CalcIDSCheme, schemes],
        [CalcIDMethod, methods],
        [CalcIDMainTarget, targets],
        [CalcIDCondition, conds],
        [CalcIDSubCondition, subconds],
    ];
    let calclabels = [];
    for(let i = 0; i < categories.length; i++){
        let category = categories[i];
        let valids = category[1].filter(item => item != SimpleLabel);
        for(let j = 0; j < category[1].length; j++){
            let label = category[1][j];
            if(label == SimpleLabel){
                continue;
            }
            let key = Object.keys(label)[0];
            let lists = [
                j == 0 ? [category[0], valids.length] : null,
                CalcLabels[category[0]][key]
            ];
            if(ispython){
                lists.push(key)
            }
            else{
                lists.push(label[key])
            }
            calclabels.push(lists);
        }
    }

    let cell, rows = [];
    let table = document.createElement("table");
    let caption = document.createElement("caption");
    caption.innerHTML = "Classification and Description of Menu Items";
    table.caption = caption;

    rows.push(table.insertRow(-1)); 
    let titles = ["Category", "GUI Menu Items"];
    let widths = ["150px", "150px", ""];
    if(ispython){
        titles.push("Simplified");
        widths = ["", "", ""];
    }
    else{
        titles.push("Details");
    }
    for(let j = 0; j < titles.length; j++){
        cell = rows[rows.length-1].insertCell(-1);
        cell.innerHTML = titles[j];    
        cell.className = " title";
        if(widths[j] != ""){
            cell.setAttribute("width", widths[j]);
        }
    }

    let links = {
        [MenuLabels.spdens]: "surfacepd.png",
        [MenuLabels.ppower]: "slittype.png",
        [MenuLabels.pflux]: "slittype.png",
        [MenuLabels.spatial]: "spatialgrid.png",
    }
    let likids = Object.keys(links);

    for(let i = 0; i < calclabels.length; i++){
        let menu = calclabels[i];
        rows.push(table.insertRow(-1));
        for(let j = 0; j < menu.length; j++){
            if(menu[j] == null){
                continue;
            }
            cell = rows[rows.length-1].insertCell(-1);
            if(Array.isArray(menu[j])){
                cell.setAttribute("rowspan", menu[j][1]);
                cell.innerHTML = menu[j][0];
            }
            else{
                if(ispython && j == 2){
                    cell.classList.add("prm");
                }
                cell.innerHTML = menu[j];
            }
        }
    }

    let retstr = table.outerHTML;
    return retstr;
}

function GetPrmListTable(labels, conts, subtitles)
{
    let table = document.createElement("table");
    let rows = [], cell;
    let titles = ["Parameter/Option", "Detail"];

    rows.push(table.insertRow(-1));
    for(let j = 0; j < titles.length; j++){
        cell = rows[rows.length-1].insertCell(-1);
        cell.innerHTML = titles[j];
        cell.className += " title";
    }

    for(let j = 0; j < conts.length; j++){
        let cont = conts[j];
        let label = labels[j];

        if(subtitles[j] != ""){
            rows.push(table.insertRow(-1));
            cell = rows[rows.length-1].insertCell(-1);
            cell.setAttribute("colspan", "2");
            if(Array.isArray(subtitles[j])){
                cell.innerHTML = subtitles[j][0];
                cell.id = subtitles[j][1];
            }
            else{
                cell.innerHTML = subtitles[j];
            }
            cell.className += " subtitle";    
        }

        for(let i = 0; i < cont.length; i++){
            for(let k = 0; k < cont[i][0].length; k++){
                rows.push(table.insertRow(-1));
                cell = rows[rows.length-1].insertCell(-1);
                let labelr = label == null ? cont[i][0][k] : label[cont[i][0][k]];
                let id;
                if(Array.isArray(labelr)){
                    cell.innerHTML = labelr[0];
                    id = labelr[0];
                }
                else{
                    cell.innerHTML = labelr;
                    id = labelr;
                }
                if(cont[i].length > 2){
                    cell.id = id;
                }
                if(k == 0){
                    cell = rows[rows.length-1].insertCell(-1);
                    if(Array.isArray(cont[i][1])){
                        cell.className += " cont";
                        let p = document.createElement("p")
                        p.innerHTML = cont[i][1][0];
                        let ul = document.createElement("ul");
                        for(let l = 1; l < cont[i][1].length; l++){
                            let li = document.createElement("li");
                            li.innerHTML = cont[i][1][l];
                            ul.appendChild(li);
                        }
                        cell.appendChild(p);
                        cell.appendChild(ul);
                    }
                    else{
                        cell.innerHTML = cont[i][1];
                    }
                    if(cont[i][0].length > 1){
                        cell.setAttribute("rowspan", cont[i][0].length.toString());
                    }
                }
            }
        }
    }
    return table.outerHTML;
}

function GetAccPrmList()
{
    let prmconts = [
        [["eGeV"], "Total energy of the electron beam."],
        [["imA", "aimA"], "Average beam current of the accelerator. The former is determined by the user, while the latter is evaluated from \"Pulses/sec\" and \"Bunch Charge\"."],
        [["cirm"], "Circumference of the storage ring."],
        [["bunches"], "Number of electron bunches stored in the storage ring."],
        [["pulsepps"], "Number of electron bunches/second in the linear accelerator."],
        [["bunchlength", "bunchcharge"], "Bunch length and charge of the electron beam."],
        [["emitt"], "Natural emittance of the electron beam."],
        [["coupl", "espread"], "Coupling constant and energy spread of the electron beam."],
        [["beta", "alpha"], "Twiss parameters at the center of the light source"],
        [["eta", "etap"], "Dispersion functions and their derivatives."],
        [["peakcurr"], "Peak current of the electron beam evaluated from relevant parameters."],
        [["epsilon"], "Horizontal and vertical emittances evaluated from &epsilon; and Coupling Constant."],
        [["sigma", "sigmap"], "Beam size and angular divergence at at the center of the light source."],
        [["gaminv"], "Inverse of the Lorentz factor."],
        [["R56add"], "Strength of the virtual dispersive section located in front of the light source. Effective for computation of coherent radiation, if "+GetQString(EtProfLabel)+" is chosen for the electron bunch profile."]
    ];
    let optconnts = [
        [["bunchtype"], 
            ["Specify the distribution functions of the electron beam in the spatial and temporal domains.",
            GetQString(GaussianLabel)+": Gaussian functions in the both domains.",
            GetQString(CurrProfLabel)+": import the current profile.",
            GetQString(EtProfLabel)+": import the electron density in the (E-t) phase space.",
            GetQString(ImportPaticleLabel)+": load the particle coordinates in the 6D phase space."]
        ],
        [["bunchdata"], "File name to specify the particle coordinates in the 6D phase space (x,x',y,y',t,DE/E) used for "+GetQString(ImportPaticleLabel)+" option. The format should be as follows."+GetDirectPara("       x        x'      y        y'        t     DE/E\n 6.20E-4 -6.08E-5 4.83E-4 -7.72E-5 -7.68E-15 -0.00133\n-2.88E-4 -1.83E-5 7.21E-4 -4.09E-5 -5.49E-15 -9.08E-4\n                ...\n 9.22E-4 -1.09E-5 0.00160 -1.47E-4  5.33E-16  3.48E-4")+"where x and y should be given in m, x' and y' in rad, t in sec, and DE/E (energy deviation) should be normalized by the average energy, and thus is dimensionless."],
        [["injectionebm"], 
            ["Specify the injection condition, or the position and angle of the electron beam at the entrance of the light source.",
            GetQString(AutomaticLabel)+": an appropriate condition for the current light source is selected. This is usually recommended in most cases.",
            GetQString(EntranceLabel)+", "+GetQString(CenterLabel)+", "+GetQString(ExitLabel)+": the electron beam axis is adjusted to coincide with that of the light source. The longitudinal position for adjustment can be selected from the entrance, center, and exit of the light source.",
            GetQString(CustomLabel)+": directly input the injection condition."]
        ],
        [["zeroemitt", "zerosprd"], " Calculation is done without the effects due to the finite emittance and/or energy spread of the electron beam."],
        [["singlee"], "Calculation is done radiation emitted from a single electron."]
    ];
    let injecprms = [
        [["xy"], "Horizontal and vertical positions at the entrance."],
        [["xyp"], "Horizontal and vertical angles at the entrance"]
    ];

    return GetPrmListTable( 
        [AccPrmsLabel, AccOptionsLabel, InjectionPrmsLabel], 
        [prmconts, optconnts, injecprms], 
        ["Parameters", "Options", "Parameters for the Injection Condition"]);
}

function GetSrcTypesTable()
{
    let cell, rows = [];
    let table = document.createElement("table");
    let caption = document.createElement("caption");
    caption.innerHTML = "List of light sources available in SPECTRA";
    table.caption = caption;

    rows.push(table.insertRow(-1)); 
    let titles = ["Name", "Details", "Field Profile"];
    for(let j = 0; j < titles.length; j++){
        cell = rows[rows.length-1].insertCell(-1);
        cell.innerHTML = titles[j];    
        cell.className = " title";
    }

    let sinfu = [
        LIN_UND_Label,
        VERTICAL_UND_Label,
        HELICAL_UND_Label,
        ELLIPTIC_UND_Label,
        FIGURE8_UND_Label,
        VFIGURE8_UND_Label
    ];
    let sinfw = [
        WIGGLER_Label,
        EMPW_Label
    ];
    let customsrc = [
        FIELDMAP3D_Label,
        CUSTOM_PERIODIC_Label,
        CUSTOM_Label
    ];

    let details = {};
    details[LIN_UND_Label] = "Conventional linear undulator for horizontal polarization";
    details[VERTICAL_UND_Label] = "Undulator for vertical polarization to generate a horizontal field";
    details[HELICAL_UND_Label] = "Undulator for circular polarization to generate a (completely) helical field";
    details[ELLIPTIC_UND_Label] = "General form of an undulator to generate a helical-like field (horizontal and vertical field amplitudes may be different)";
    details[FIGURE8_UND_Label] = "Undulator having figure-8 shaped electron orbit, for horizontal polarization and low on-axis heat load";
    details[VFIGURE8_UND_Label] = "Same as the figure-8 undulator, but for vertical polarization";
    details[MULTI_HARM_UND_Label] = "\"Semi-Customized\" undulator, in which the magnetic field distribution is composed of a number of harmonic components. The strength and phase of each harmonic should be defined by the user.";
    details[WIGGLER_Label] = "Conventional multi-pole wiggler";
    details[EMPW_Label] = "Elliptic multi-pole wiggler for elliptic polarization in the high energy region";
    details[WLEN_SHIFTER_Label] = "Wavelength shifter composed of 3 magnet poles; the main (central) pole has the strongest field, while the other two have lower fields so that the field integrals are zero. Note that the magnetic field is not uniform along the longitudinal (z) axis but changes in a sinusoidal manner";
    details[BM_Label] = "Conventional bending magnet";
    details[FIELDMAP3D_Label] = "Specify the 3-D magnetic vector in the (x,y,z) space to calculate the electron orbit. Refer to *** for details.";
    details[CUSTOM_PERIODIC_Label] = "Similar to \""+FIELDMAP3D_Label+"\", but specify the 2D magnetic vector along z. Refer to *** for details.";
    details[CUSTOM_Label] = "";

    for(const src of SrcTypels){
        rows.push(table.insertRow(-1)); 
        
        cell = rows[rows.length-1].insertCell(-1);
        cell.innerHTML = src;

        if(src != CUSTOM_Label){
            cell = rows[rows.length-1].insertCell(-1);
            if(Array.isArray(details[src])){
                cell.innerHTML = WriteObject(0, details[src]);
            }
            else{
                cell.innerHTML = details[src];
            }
            if(src == CUSTOM_PERIODIC_Label){
                cell.setAttribute("rowspan", "2");
            }
        }

        if(sinfu.indexOf(src) > 0 || sinfw.indexOf(src) > 0 || customsrc.indexOf(src) > 0)
        {
            continue;
        }
        cell = rows[rows.length-1].insertCell(-1);
        if(src == sinfu[0] || src == sinfw[0]){
            cell.innerHTML = "Sinusoidal";
            if(src == sinfu[0]){
                cell.setAttribute("rowspan", sinfu.length.toString());
            }
            else{
                cell.setAttribute("rowspan", sinfw.length.toString());
            }
        }
        else if(src == customsrc[0]){
            cell.innerHTML = "Custom";
            cell.setAttribute("rowspan", customsrc.length.toString());
        }
        else if(src == SrcTypeLabel.BM){
            cell.innerHTML = "Uniform";
        }
        else if(src == SrcTypeLabel.WLEN_SHIFTER){
            cell.innerHTML = "Semi Sinusoidal";
        }
        else{
            cell.innerHTML = "Custom";
        }
    }
    return table.outerHTML;
}

function GetSrcPrmList()
{
    let bmsche = WriteFigure("BMsetup.png", "Schematic drawing of the bending magnet configuration.", true);
    let prmconts = [
        [["gap"], "Gap of the ID."],
        [["bxy", "b"], "Field amplitude (IDs) or uniform field (BMs)."],
        [["bmain", "subpoleb"], "Peak fields of the main and sub poles of Wavelength Shifters."],
        [["lu"], "Magnetic Period Length of the ID"],
        [["devlength"], "Total length of the ID"],
        [["reglength"], "Length of the ID for the regular period."],
        [["periods"], "Number of regular periods."],
        [["Kxy0"], "Available for APPLE undulators. Maximum K values (deflection parameters) when the phase is adjusted to generate horizontal and vertical polarizations."],
        [["phase"], "Longitudinal shift of each magnetic array for the APPLE undulators, defined as the displacement from the position for the horizontally-polarized mode. To be specific, K values are given as $K_x=K_{x0}\\sin(2\\pi\\Delta z/\\lambda_u)$ and $K_y=K_{y0}\\cos(2\\pi\\Delta z/\\lambda_u)$, where $\\Delta z$ is the phase shift."],
        [["Kxy", "K"], "K values of the ID."],
        [["Kperp"], "Composite K value defined as $\\sqrt{K_x^2+K_y^2}$."],
        [["e1st","lambda1"], "Fundamental photon energy and wavelength of undulator radiation."],
        [["multiharm"], [
                "Arrange the harmonic components for "+SrcTypeLabel.MULTI_HARM_UND+"s.",
                "K<sub>x</sub> Ratio ($=R_n$) and Phase ($=P_n$, in degrees) refer to the fraction and phase of the horizontal field of the n-th harmonic component, where n is the number indicated in the 1st row.",
                "The K value corresponding to the n-th harmonic is defined as \\[K_{xn}=K_x\\frac{R_n}{\\sqrt{R_1^2+R_2^2+\\cdots+R_N^2}},\\] where $K_x$ is the (total) K value and $N$ is the maximum harmonic number.",
                "The field distribution is defined as \\[B_{x}(z)=\\sum_{n=1}^{N}B_{xn}\\sin\\left[2\\pi\\left(\\frac{nz}{\\lambda_u}+\\frac{P_n}{360}\\right)\\right],\\] where $B_{xn}$ is the peak field corresponding to the K value of the n-th harmonic.",
                "Similar definitions of $K_{yn}$ and $B_{y}(z)$."
            ]
        ],
        [["radius"], "Radius of the BM."],
        [["bendlength", "fringelen", "csrorg"], "Specify the geometric configuration of BMs. \"Origin for CSR\" defines the longitudinal coordinate where the electron bunch length or the temporal profile is defined to calculate coherent radiation."+bmsche],
        [["mplength", "subpolel"], "Lengths of the main and sub poles of the Wavelength Shifter."],
        [["bminterv"], "Distance between two BMs."],
        [["fmap"], "File name for the 3D magnetic field data, which defines the magnetic vector $\\boldsymbol{B}(\\boldsymbol{r})$. The format should be as follows."+GetDirectPara("0.2	0.3	0.5	11	13	421\n1.23456e-1	2.3456e-1	3.4557e-1\n2.23456e-1	3.3456e-1	6.4557e-1\n	...\n4.23456e-1	5.3456e-1	8.4557e-1\n2.23456e-1	3.3456e-1	6.4557e-1")+"The 6 numbers in the first line indicate the grid interval in mm and number of grid points along the x, y, and z axes. In the above case, the magnetic field components are given at 11x13x421 grid points with the x, y, and z intervals of 0.2 mm, 0.3 mm, and 0.5 mm, respectively. From the 2nd line, the magnetic field components ($B_x$, $B_y$, $B_z$) at each grid point are given. The grid point should be moved first along the z direction, next y direction, and finally x direction."],
        [["sigmar", "sigmarx", "sigmary"], "Natural source size and angular divergence of radiation."],
        [["Sigmax", "Sigmay"], "Effective source size and angular divergence of the photon beam, convoluted with those of the electron beam."],
        [["fd", "flux", "brill"], "Approximate values of the on-axis flux density, available flux, and brilliance at &epsilon;<sub>1st</sub>."],
        [["pkbrill"], "Peak brilliance at &epsilon;<sub>1st</sub> evaluated with the peak current of the electron beam."],
        [["degener"], "Bose degeneracy evaluated for the Peak Brilliance."],
        [["ec", "lc"], "Critical photon energy and wavelength."],
        [["tpower"], "Total radiation power."],
        [["tpowerrev", "linpower"], "Total power/revolution and linear power density of the BM."]
    ];

    let slitsche = WriteFigure("segscheme.png", "Schematic drawing of the segmented undulator configurations: (a) all segments are identical, and (b) even-number segments are of different type.", true);
    let optconnts = [
        [["gaplink"], 
            ["Specify the relation between the gap and peak field of the ID.",
            GetQString(NoneLabel)+": no relation is given. The Gap parameter is not available.",
            GetQString(AutomaticLabel)+": evaluate according to an analytical formula of Halbach array defined as \\[B(g)=1.8G B_r\\mbox{exp}(-\\pi g/\\lambda_u),\\] where $B_r$ is the remanent field of the magnet and $G$ is a geometrical (reduction) factor coming from the physical boundary conditions such as the finite dimension of magnet blocks.",
            GetQString(ImpGapTableLabel)+": evaluate by interpolating the imported data."],
            true // <- enable id
        ],
        [["apple"], "Enable/disable the APPLE configuration for "+ELLIPTIC_UND_Label+"s."],
        [["field_str"], 
            ["Specify the field-distribution symmetry of the ID. ",
            GetQString(AntiSymmLabel)+": anti-symmetric with respect to the center (sine-like).",
            GetQString(SymmLabel)+": symmetric with respect to the center (cosine-like)."]
        ],
        [["endmag"], "Put additional magnets at the both ends, for orbit compensation."],
        [["natfocus"], 
            ["Apply the natural focusing of IDs.",
            GetQString(NoneLabel)+": no focusing considered.",
            GetQString(BxOnlyLabel)+": horizontal field (and focusing).",
            GetQString(ByOnlyLabel)+": vertical field (and focusing).",
            GetQString(BothLabel)+": focus in the both directions.",
            ]
        ],
        [["fielderr"], "Specify the magnetic error components for undulators."],
        [["phaseerr"], "Specify the RMS phase error and relevant parameters for undulators."],
        [["bmtandem"], "Calculate radiation from two BMs located at the both ends of the straight section."],
        [["segment_type"], 
            ["Arrange the segmented undulator configuration. For details of how these segmentation schemes work to improve the characteristics of radiation, refer to "+GetLink("refsegment", refidx.refsegment, false)+" and "+GetLink("refsegx", refidx.refsegx, false)+"."+slitsche+
            "To adjust the optical phase ($\\Delta\\phi$) in each drift section, SPECTRA assumes that a phase shifter, or a 1.5-period undulator with the same periodic length, is installed at the center of the drift section, whose amplitude is tuned to generate the specified phase. Five options are available as explained below.",
            GetQString(NoneLabel)+": no segmentation.",
            GetQString(IdenticalLabel)+": all segments have the same specification (a).",
            GetQString(SwapBxyLabel)+": horizontal and vertical fields are swapped in even segments (b).",
            GetQString(FlipBxLabel)+": polarity of the horizontal field is swapped in even segments (b).",
            GetQString(FlipByLabel)+": polarity of the vertical field is swapped in even segments (b).",
            ],
            true // <- enable id
        ],
        [["perlattice"], "The betatron function is periodic with the period of segment interval."]
    ];

    let ferrprms = [
        [["boffset"], "Magnetic field offset, such as that coming from the ambient field."],
        [["ltaper", "qtaper"], "Linear (a<sub>1</sub>) and quadratic (a<sub>2</sub>) taper coefficients. The magnetic field amplitude is given as \\[B(z)=B_0(1+a_1z+a_2z^2),\\] where $B_0$ is the field amplitude corresponding to the K value."]
    ];

    let perrprms = [
        [["seed"], "Seed for the random number generator to model the field error."],
        [["fsigma"], "RMS of the peak field variation."],
        [["psigma"], "RMS of the phase error "+GetLink("refperr", refidx.refperr, false)+"."],
        [["xysigma"], "RMS of the trajectory error."]
    ];

    let segprms = [
        [["segments", "hsegments"], "Number of undulator segments (M) if "
            +GetQString(IdenticalLabel)+" is selected for "+GetQString(SrcPrmsLabel.segment_type[0])
            +", or number of segment pair (M') for other options."],
        [["interval"], "Distance between the center positions of adjacent undulator segments."],
        [["pslip"], "Slippage in the drift section given in the unit of &lambda;<sub>1st</sub>."],
        [["phi0"], "Additional phase in the unit of &pi;."],
        [["phi12"], "Additional phase in the unit of &pi;: subscripts 1 and 2 refer to the odd and even drift sections"],
        [["mdist"], "Distance between virtual focusing magnets in the matching section to arrange the periodic lattice function."]
    ];

    return GetPrmListTable( 
        [SrcPrmsLabel, SrcPrmsLabel, FerrPrmsLabel, PerrPrmsLabel, SegPrmsLabel], 
        [prmconts, optconnts, ferrprms, perrprms, segprms], 
        ["Parameters", "Options", 
            "Parameters for the Field-Error Condition",
            "Parameters to Specify the Phase Error",
            "Parameters for the "+GetLink(SrcPrmsLabel.segment_type[0], "Segmented Undulator",false)+" Option"
        ]);
}

function GetConfigPrmList()
{
    let slitsche = WriteFigure("slittype.png", "Schematic drawing of the slit conditions.", true);
    let spdmesh = WriteFigure("spatialgrid.png", "Meanings of the observation position for "+GetQString(MenuLabels.spatial)+": (a) [Planar Surface: x-z/y-z] and (b) [Cylindrical Surface].", true);
    let spdgrid = WriteFigure("surfacepd.png", "Observation conditions of the surface power density.", true);
    let spdpoint = WriteFigure("surfacepd_point.png", "Observation conditions of the surface power density available in "+FixedPointLabel+" calculation.", true);
    let fpsche = WriteFigure("fourieplane.png", "Virtual observation in the Fourier plane.", true);
    let vpdsche = WriteFigure("volpdens.png", "Definitions of parameters to define the condition of the target object and coordinate to define the calculation positions in "+MenuLabels.vpdens+" calculations", true);
    let felsche = WriteFigure("felsteps.png", "Definitions of parameters to define the longitudinal steps to solve the FEL equation.", true);
    let prmconts = [
        [[
            "xyfix",
            "qxyfix"       
        ], "Transverse position/angle at the observation point."],
        [[
            "erange",
            "de"        
        ], "Energy range and pitch for "+MenuLabels.energy+" calculations."],
        [["epitch"], "Energy pitch for integration in "+MenuLabels.vpdens+" calculations. Needs to be defined by the user for "+CUSTOM_Label+" light sources."],
        [["emesh"], "Number of energy points for "+MenuLabels.energy+" calculations."],
        [["detune"], "Photon energy defined as a detuned value, i.e., $\\varepsilon/(n\\varepsilon_1)-1$, where $n$ is the target harmonic number."],
        [["efix"], "Photon energy to be fixed."],
        [["nefix"], "Same as the above, but normalized by &epsilon;<sub>1st</sub>."],
        [[
            "xrange",
            "qxrange", 
            "yrange",
            "qyrange",
            "rrange",
            "qrange",
            "phirange"
        ], "Range of the Observation positions/angles for \"Spatial Dependence\" calculations: (a) [Along Axis] and [Mesh: x-y] and (b) [Mesh: r-&phi;]."+spdmesh],
        [[
            "xmesh", 
            "ymesh",
            "rphimesh",
            "qphimesh",
            "phimesh"
        ], "Number of observation point in the relevant range."],
        [["slit_dist"], "Distance from the center of the light source to the observation point."],
        [[
            "slitpos",
            "qslitpos",
            "nslitapt",
            "slitapt",
            "slitr",
            "slitq"
        ], "Specify the configuration of the slit positions and aperture."+slitsche],
        [[
            "drange",
            "dmesh"        
        ], "Depth range and number of points for "+MenuLabels.vpdens+" calculations."],
        [[
            "qslitapt",
            "illumarea"    ,
            "Qgl",
            "Phiinc"    
        ], "Angular acceptance to confine the photon beam and resultant illuminated area of the object, and angles to define the condition of glancing incidence for "+MenuLabels.vpdens+" calculations."+vpdsche+"Azimuth of Incidence define the direction along which the object is inclined: if it is vertically tilted as in the case of a crystal monochromator, this parameter should be 90 degree, as shown in the above figure."],
        [[
            "xrange",
            "yrange",
            "zrange",
            "spdxfix",
            "spdyfix",
            "spdrfix"
        ], "Position of the object and range of observation for "+MenuLabels.pdenss+" calculations. Note that SPECTRA distinguishes the inner and outer sides of the surface. To be specific, the above figure shows the case when the inner size indicated by a red line is facing the beam axis, and thus receives the radiation power. If, in contrast, the object with the same normal vector is located at a negative position of x, the inner surface is facing outsize and it does not receive any radiation"+spdgrid],
        [[
            "xmesh", 
            "ymesh",
            "zmesh",
        ], "Number of observation points in the relevant range"],
        [[
            "Qnorm",
            "Phinorm"    
        ], "Normal vectors to specify the inner surface of the object irradiated by SR. In "+GetQString(FixedPointLabel)+" calculations, the normal vector to the object surface is specified more flexibly by two angles as schematically illustrated below. For example, &Theta; = &Phi; = 0 means that the surface of the object is parallel to the y-z plane, with its inner side facing the beam axis. Angles of the normal vector to define the inner surface illuminated by radiation for "+MenuLabels.pdenss+" calculations."+spdpoint],
        [[
            "fsize",
            "fdiv"        
        ], "Photon beam size and divergence at the observation position, defined at &epsilon;<sub>1st</sub>. Note this is a rough estimation and does not take into account the energy spread of the electron beam."],
        [[
            "psize",
            "pdiv"        
        ], "Spatial spread and divergence of the radiation power at the observation position"],
        [[
            "krange",
            "ckrange",
            "kmesh"    
        ], "Range of the K values and number of points."],
        [["e1strange"], "Range of the fundamental energy determined by the above K-value range."],
        [["pplimit"], "Upper limit of the partial power to define the width and height of the rectangular slit for "+MenuLabels.Kvalue+" calculations."],
        [[
            "hrange",
            "hfix"
        ], "Harmonic range or target harmonic number for K-value dependence calculations."],
        [[
            "trange",
            "tmesh"        
        ], "Temporal range and number of points for "+MenuLabels.temporal+" calculations."],
        [["hmax"], "Maximum harmonic number to be considered."],
        [[
            "Xfix",
            "Yfix",
            "Xpfix",
            "Ypfix"        
        ], "Transverse positions and angles at the source point where the Wigner function is calculated. These parameters should be distinguished from those indicated by lower letters, which mean the transverse positions at a certain longitudinal position downstream of the light source."],
        [[
            "Xrange",
            "Xmesh",
            "Xprange",
            "Xpmesh",
            "Yrange",
            "Ymesh",
            "Yprange",
            "Ypmesh"
        ], "Calculation range/number of points of the transverse positions/angles at the source point. Should be distinguished from those indicated by lower letters (see above)."],
        [[
            "gtacc",
            "horizacc"        
        ], "Angular acceptance normalized by &gamma;<sup>-1</sup> to calculate the Wigner function."]
    ];

    let optconnts = [
        [["filter"], 
            ["Specify the type of filtering.",
            GetQString(NoneLabel)+": no filter is assumed.",
            GetQString(GenFilterLabel)+": slab or layer that attenuates the photon beam, made of any material.",
            GetQString(BPFGaussianLabel)+": Gaussian bandpath filter.",
            GetQString(BPFBoxCarLabel)+": boxcar-type bandpath filter.",
            GetQString(CustomLabel)+": evaluate the transmission rate by interpolating the imported data.",
            ]
        ],
        [["estep", "dstep"],
            ["Specify how to change the energy/depth position in the calculation range.",
                GetQString(LinearLabel)+": linear variation (constant interval).",
                GetQString(LogLabel)+": logarithmic variation (constant ratio)."
            ]
        ],
        [["aperture"],
            ["Specify how to represent the width and height of the rectangular slit.",
                GetQString(FixedSlitLabel)+": fixed aperture",
                GetQString(NormSlitLabel)+": normalized by "+ConfigPrmsLabel.fsize+" and is varied for "+MenuLabels.Kvalue+" calculations"
            ]
        ],
        [["defobs"],
            [
                "Specify how to represent the transverse observation points.",
                GetQString(ObsPointDist)+": in position.",
                GetQString(ObsPointAngle)+": in angle."
            ]
        ],
        [["normenergy"], "Specify the photon energy as a normalized value."],
        [["powlimit"], "Put an upper limit on the allowable partial power."],
        [["optDx"], "Horizontal angular acceptance is virtually closed to reduce the computation time, without changing the calculation results."],
        [["xsmooth"], "Apply smoothing for the Wigner function of BMs and wigglers; larger values results in more smooth profiles."],
        [["fouriep"], "Calculation is done at the \"Fourier Plane\" as schematically illustrated below, to evaluate the angular profile at the source point (center of the light source)"+fpsche],
        [["wiggapprox"], "Apply the wiggler approximation, in which radiation incoherently summed up (as photons)."],
        [["esmooth"], "Apply the spectral smoothing; this is useful to reduce the computation time by smoothing the spectral fine structure potentially found in undulator radiation."],
        [["smoothwin"], "Smoothing window in %; this means that the photon flux at 1000 eV is given as the average from 995 to 1005 eV."],
        [["accuracy"], "Specify the numerical accuracy. In most cases, "+GetQString(DefaultLabel)+" is recommended, in which case SPECTRA automatically arranges all the relevant parameters. If "+GetQString(CustomLabel)+" is selected, the user should configure each parameter. Refer to "+GetLink(EditAccuracy, EditAccuracy, false)+" for details.", true],
        [["CMD"], "Perform "+GetQString(CMDLabel)+" after calculating the Wigner function."],
        [["CMDfld"], 
            [
                "Calculate and export the modal profiles based on the CMD results",
                GetQString(NoneLabel)+": do not export.",
                GetQString(JSONOnly)+": export in the JSON format.",
                GetQString(BinaryOnly)+": export in the "+GetLink(sections.binary, "binary format", false)+".",
                GetQString(BothFormat)+": export in the both formats."
            ]
        ],
        [["CMDint"], "Calculate and export the modal intensity profiles based on the CMD results"],
        [["CMDcmp"], "Reconstruct the Wigner function using the CMD result to check its validity."],
        [["CMDcmpint"], "Reconstruct the flux density profile using the CMD result to check its validity."],
        [["GSModel"], "Use Gaussian-Schell (GS) model to simplify the CMD and reduce computation time."],
        [["GSModelXY"], 
            [
                "Use Gaussian-Schell (GS) model for CMD. Select the axis to apply.",
                GetQString(NoneLabel)+": do not use GS model.",
                GetQString(XOnly)+": GS model for horizontal axis.",
                GetQString(YOnly)+": GS model for vertical axis.",
                GetQString(BothFormat)+": GS model for both axes."
            ]
        ],
        [["fel"], 
            ["Coherent radiation in an FEL (free electron laser) mode is calculated. If this option is enabled, interaction (energy exchange) between electrons and radiation is taken into account in solving the equation of electron motion in the 6D phase space. This is exactly what the general FEL simulation code does (solving the FEL equation), and thus the amplification process in FELs can be evaluated. There are several types of FEL modes available in SPECTRA, depending on how to prepare the initial condition. Note that the self-amplified spontaneous emission (SASE) FELs cannot be evaluated; this comes from the difficulty in dealing with the shot-noize, which is the source of amplification in SASE FELs.",
                GetQString(FELPrebunchedLabel)+": the electron beam is pre-bunched and no seed light is supposed.",
                GetQString(FELSeedLabel)+": a simple seed pulse is supposed.",
                GetQString(FELCPSeedLabel)+": same as the above, but the seed pulse is chirped.",
                GetQString(FELDblSeedLabel)+": same as the above, but a couple of pulses are supposed.",
                GetQString(FELReuseLabel)+": reuse the bunch factor evaluated in the former calculations. This option is available by opening a former calculation result of coherent radiation,  with the FEL mode option enabled."
            ], true
        ],
        [["exportInt"], "Export the intermediate data evaluated during the process of solving the FEL equation.", true],
        [["R56Bunch"], "Export the bunch profile after the electron beam passes through a virtual dispersive section located downstream of the source, as in the high-gain harmonic generation (HGHG) FELs.", true],
        [["exportEt"], "Export the electron density in the (E-t) phase space."],
    ];

    let bpfprms = [
        [["bpfcenter"], "Central photon energy of the bandpath filter (BPF)."],
        [["bpfwidth"], "Full width of the boxcar-type BPF."],
        [["bpfsigma"], "1&sigma; of the Gaussian BPF."],
        [["bpfmaxeff"], "Maximum transmission rate of the BPF."]
    ];

    let cmdprms = [
        [["HGorderxy", "HGorderx", "HGordery"], "Upper limit of the order of the Hermite-Gaussian functions to be used in the CMD."],
        [["maxmode"], "Maximum number of the coherent modes for post-processing (exporting the modal profile, reconstructing the Wigner functions)."],
        [["cutoff"], "Cutoff amplitude (normalized) of individual modes, below which Hermite-Gaussian functions are neglected."],
        [["fieldgridxy", "fieldgridx", "fieldgridy"], "Intervals of spatial grid points to export the modal profile."]
    ];

    let felprms = [
        [["pulseE"], "Seed pulse energy."],
        [["wavelen"], "Seed wavelength."],
        [["pulselen"], "Seed pulse length."],
        [["tlpulselen"], "Transform-limited pulse length of the chirped seed pulse."],
        [["srcsize"], "Seed source size."],
        [["waistpos"], "Longitudinal position where the seed pulse forms a beam waist."],
        [["timing"], "Relative time of the seed pulse with respect to the electron beam."],
        [["gdd", "tod"], "Group delay dispersion and third order dispersion of the chirped seed pulse."],
        [["pulseE_d"], "Pulse energies of the 1st and 2nd seed pulses. Available when "+GetQString(FELDblSeedLabel)+" is chosen. Note that there are a number of parameters having the same suffix (1,2), which denotes that they are for the 1st and 2nd seed pulses."],
        [["svstep","radstep"], "Define the longitudinal step to solve the FEL equation. Refer to the schematic drawing for details."+felsche+"The light source is divided into a number of steps (indicated by yellow arrows), and each step is further divided into a number of substeps (blue arrows). The bunch factor of the electron beam is assumed to be constant within a step and is updated at the end, which is then used to calculate the coherent radiation in the next step. The radiation waveform is assumed to be constant within a substep besides the slippage effect and is updated at the end, which is then used to evaluate the interaction with electrons in the next substep. A number of data sets used in each step is saved in the output file, if "+GetLink(ConfigOptionsLabel.exportInt[0], ConfigOptionsLabel.exportInt[0], false)+" option is enabled."],
        [["eproi"], "Photon energy range of interest to solve the FEL equation."],
        [["particles"], "Number of macro-particles to represent the electron beam."],
        [["edevstep"], "Interval of the electron energy deviation to export the electron density in the (E-t) phase space."],
        [["R56"], "Strength of the virtual dispersive section. Need to be specified if "+GetLink(ConfigOptionsLabel.R56Bunch[0], ConfigOptionsLabel.R56Bunch[0], false)+" option is enabled."]
    ];

    return GetPrmListTable( 
        [ConfigPrmsLabel, ConfigOptionsLabel, BPFPrmsLabel, CMDPrmsLabel, FELPrmsLabel], 
        [prmconts, optconnts, bpfprms, cmdprms, felprms], 
        ["Parameters", "Options", "Parameters to Specify the BPF", ["Parameters for the CMD (coherent mode decomposition)", CMDParameterLabel], "Parameters for the FEL mode"]);
}

function GetOutputPrmList()
{
    let outprms = [
        [["format"], "Select the format of the output file from three options: \"JSON\" for the JSON format, \"ASCII\" for the ASCII (simple text with the suffix \".txt\") format, and \"Both\" for the both options. Note that the ASCII format is identical to that in the older (&lE 10.2) versions, however, it cannot be used later for "+GetLink(sections.postproc, sections.postproc, false)+" (visualization of the data)."],
        [["folder", "prefix", "serial"], "Input the location of the output file in [Folder], a prefix text in [Prefix], and a serial number in [Serial Number]. Then the output file name is given as [Folder]/[Prefix]-[Serial Number].[Format], like \"/Users/data/test-1.json\", where \"/Users/data\", \"test\", 1, and \"json\" refer to [Folder], [Prefix], [Serial Number] and [Format]. Note that the serial number can be -1 (negative), in which case it is not attached to the data name."],
        [["comment"], "Input any comment in [Comment] if necessary, which is saved in the output file and can be referred later on."]
    ];

    return GetPrmListTable([OutputOptionsLabel], [outprms], [""]);
}

function GetOutputItems()
{
    let outitems = [
        [["Flux Density"], "Spatial (far field conditions) or angular (others) flux density"],
        [["Flux"], "Partial photon flux passing through a finite angular acceptance, or total flux integrated over the whole solid angle"],
        [["GA. Brilliance", "Brilliance"], "Photon density in the 4D phase space (or its maximum). \"GA.\" stands for \"Gaussian Approximation\", meaning that it is evaluated by assuming that the photon beam is a Gaussian one."],
        [["Prj. Brilliance"], "Brilliance projected on the (X,X') or (Y,Y') phase space."],
        [["PL(s1/s0)", "PC(s3/s0)", "PL45(s2/s0)"], "Stokes parameters: PL, PC, PL45 correspond to the horizontal, left-hand and 45-deg.-inclined linear polarizations."],
        [["Harmonic Energy", "Peak Energy"], "Photon energy of a target harmonic. \"Harmonic\" is defined as n&epsilon;<sub>1st</sub>, where n is the harmonic number, while \"Peak\" specifies the photon energy at which the photon intensity (flux density of flux) becomes the maximum; in general this is slightly lower than the former one."],
        [["Power Density"], "Spatial (far field conditions) or angular (others) power density"],
        [["Partial Power", "Total Power"], "Partial power passing through a finite angular acceptance, or total power integrated over the whole solid angle"],
        [["Harmonic Power (x)", "Harmonic Power (y)"], "Angular power density corresponding to a specific harmonic and polarization state"],
        [["Volume Power Density"], "Refer to "+GetLink(MenuLabels.vpdens, MenuLabels.vpdens, false)],
        [["Natural Size", "Natural Divergence"], "Source size and angular divergence of radiation emitted by a single electron"],
        [["Horizontal Size", "Vertical Size"], "Source size of a photon beam emitted by an electron beam with finite emittance and energy spread"],
        [["Horizontal Divergence", "Vertical Divergence"], "Angular divergence of a photon beam"],
        [["Coherent Flux"], "Photon flux contained in a coherent volume of radiation that is fully coherent in space"],
        [["Coherent Power"], "Power contained in a bandwidth corresponding to 1 &mu;m coherence length"],
        [["Horizontal Coherent Fraction", "Vertical Coherent Fraction"], "Quality of a photon beam in terms of coherence, defined as $\\Sigma_x\\Sigma_{x'}/(\\lambda/4\\pi)$ for the horizontal direction and a similar expression for the vertical direction, where $\\Sigma_{x}$ and $\\Sigma_{x'}$ are the source size and angular divergence of the photon beam."],
        [["Harmonic Number"], "Harmonic number to generate the maximum photon intensity at a given photon energy"],
        [["Observer Time"], "Time in the laboratory frame (for observer)"],
        [["Horizontal Electric Field", "Vertical Electric Field"], "Electric field of radiation"],
        [["Horizontal Real Field", "Horizontal Imaginary Field", "Vertical Real Field", "Vertical Imaginary Field"], "Complex amplitude of radiation evaluated at a given photon energy"],
        [["Separability"], "Refer to "+GetLink(sections.separa, sections.separa, false)],
        [["Deg. Coherence (X)", "Deg. Coherence (Y)", "Deg. Coherence (Total)"], "Refer to "+GetLink(sections.degcoh, sections.degcoh, false)],
    ];
    return GetPrmListTable([null], [outitems], [""]);
}

function GetOutDataInf()
{
    let caption = "Format of the "+GetQString(OutputLabel)+" object";
    let titles = ["Key", "Details", "Format"];
    let outdata = [
        [DataDimLabel, "Dimension of the calculation data, or the number of independent variables.", "number"],
        [DataTitlesLabel, "Titles of individual arrays included in the "+GetQString(DataLabel)+" object.", "array (1D)"],
        [UnitsLabel, "Units of individual arrays included in the "+GetQString(DataLabel)+" object.", "array (1D)"],
        [DetailsLabel, "Additional information of the 3D-array data, which is generated in several calculation types. For example, those with "+GetQString(MenuLabels.tgtharm)+" (flux specific to a specific harmonic) result in a number of data, each of which is 2D and corresponds to the harmonic number.", "array (1D)"],
        [DataLabel, "Main body of the calculation result data.", "array (2D or 3D)"]
    ];
    return GetTable(caption, titles, outdata);
}

function GetAccPrmTable()
{
    let noinput = [];
    noinput.push(AccPrmsLabel.aimA[0]);
    noinput.push(AccPrmsLabel.cirm[0]);
    noinput.push(AccPrmsLabel.peakcurr[0]);
    noinput.push(AccPrmsLabel.epsilon[0]);
    noinput.push(AccPrmsLabel.sigma[0]);
    noinput.push(AccPrmsLabel.sigmap[0]);
    noinput.push(AccPrmsLabel.gaminv[0]);
    let hide = [AccPrmsLabel.minsize];
    let data = (new AccPrmOptions()).GetReferenceList(AccLabelOrder, noinput, hide, false, "");
    return data;
}

function GetSrcPrmTable()
{
    let noinput = [];
    noinput.push(SrcPrmsLabel.reglength);
    let jini = SrcLabelOrder.indexOf("sigmar");
    for(let j = jini; j < SrcLabelOrder.length; j++){
        noinput.push(SrcPrmsLabel[SrcLabelOrder[j]]);
    }
    let hide = [];
    let data = (new SrcPrmOptions()).GetReferenceList(SrcLabelOrder, noinput, hide, false, "");
    return data;
}

function GetConfigPrmTable()
{
    let noinput = [];
    noinput.push(ConfigPrmsLabel.illumarea);
    noinput.push(ConfigPrmsLabel.e1strange);
    noinput.push(ConfigPrmsLabel.fsize);
    noinput.push(ConfigPrmsLabel.psize);
    noinput.push(ConfigPrmsLabel.fdiv);
    noinput.push(ConfigPrmsLabel.pdiv);
    let hide = [];
    let data = (new ConfigPrmOptions()).GetReferenceList(ConfigLabelOrder, noinput, hide, false, "");
    return data;
}

function GetOutFilePrmTable()
{
    let noinput = [];
    let hide = [];
    let data = (new OutFileOptions()).GetReferenceList(OutputOptionsOrder, noinput, hide, false, "");
    return data;
}

function GetMenu(baseobj)
{
    let data = "";
    for(let j = 0; j < baseobj.length; j++){
        let subsections = Object.values(baseobj[j])[0];
        let isobj = false;
        for(let i = 0; i < subsections.length; i++){
            if(typeof subsections[i] != "string" 
                    && Array.isArray(subsections[i]) == false){
                isobj = true;
                continue;
            }
        }
        if(!isobj){
            let div = document.createElement("div");
            div.appendChild(GetLink(Object.keys(baseobj[j])[0], Object.keys(baseobj[j])[0], true));
            data += div.outerHTML;
            continue;
        }
        let details = document.createElement("details");
        let summary = document.createElement("summary");
        summary.innerHTML = Object.keys(baseobj[j])[0];
        details.appendChild(summary);
        let list = document.createElement("ul");
        for(let i = 0; i < subsections.length; i++){
            let item = document.createElement("li");
            if(typeof subsections[i] == "string"){
                continue;
            }
            let link = GetLink(Object.keys(subsections[i])[0], Object.keys(subsections[i])[0], true);
            item.appendChild(link);
            list.appendChild(item);
        }
        details.appendChild(list);
        data += details.outerHTML;
    }  
    return data;
}

function GetFileMenu()
{
    let caption = "Contents of \"File\" main menu. SA and WA stands for the stand-alone and web-application modes, respectively.";
    let titles = ["Menu", "Details"];
    let filemenus = [
        [MenuLabels.new, "Start SPECTRA with a default parameter set."],
        [MenuLabels.open, "Open a SPECTRA parameter file; those for older (&lE; 10.2) versions are not accepted. Please convert them first with \"Convert Parameter Files\" command."],
        [MenuLabels.append, "Append the parameter sets in another parameter file (ver. &lE; 10.2 not accepted) to the current ones."],
        [MenuLabels.loadf, "Load the output file of a former calculation."],
        [MenuLabels.outpostp, "For visualization"],
        [MenuLabels.wig, "For CMD"],
        [MenuLabels.CMDr, "For postprocessing the CMD result"],
        [MenuLabels.bunch, "For coherent radiation calculation"],
        [MenuLabels.save, "Save all the parameters and options in the current file."],
        [MenuLabels.saveas, "Save all the parameters and options in a new file."],
        [MenuLabels.exit, "Quit SPECTRA and Exit", "Both"]
    ];
    return GetTable(caption, titles, filemenus);
}

function GetRunMenu()
{
    let caption = "Contents of \"Run\" main menu";
    let titles = ["Menu", "Details"];
    let filemenus = [
        [MenuLabels.process, "Create "+CalcProcessLabel+" with the current parameters and options."],
        [MenuLabels.export, "Export the current parameters and options to a file, which can be used as an input file to directly call the solver."],
        [MenuLabels.start, "Start a new calculation, or launch the "+CalcProcessLabel+"."]
    ];
    return GetTable(caption, titles, filemenus);
}

function GetSetupDialog()
{
    let caption = "Setup Dialogs opened by running a submenu of \"Edit\" menu";
    let titles = ["Submenu", "Details"];
    let dlgconts = [
        [EditMaterial, [
            "Open a dialog to edit the material available for the filters and absorbers.",
            WriteFigure("editmaterial.png", "Dialog to edit the material for the filters and absorbers.", false),
            "In SPECTRA, a number of built-in materials are available (gray-painted ones), which cannot be edited.",
            "To add a new material, input its name and density in an empty column, together with the atomic number (Z) and mass ratio (Ratio) of each element constituting the material. The total amount of the mass ratio should be 1. The numbers of columns (materials) and rows (elements) are automatically increased when necessary."
        ]],
        [EditFiltPlotConfig, [
            "Open a dialog to configure how to plot the transmission (absorption) rate of the filter (absorber) currently specified.",
            WriteFigure("filtplot.png", "Dialog for configuration of the transmission/absorption plot.", false),
            "If \"Automatic\" is chosen, SPECTRA automatically determines the energy range and number of points."
            ], EditFiltPlotConfig
        ],
        [EditMagnet, [
            "Open a dialog to edit the configuration of magnets for undulators and wigglers to be used in calculating the relation between the gap and field amplitude, when "+GetQString(AutomaticLabel)+" is selected for "+GetLink(SrcPrmsLabel.gaplink[0], SrcPrmsLabel.gaplink[0])+".",
            WriteFigure("magconf.png", "Dialog to edit the configuration of magnets for undulators and wigglers.", false),
            "Here, B<sub>r</sub> is the remanent field of the magnet material and Geometrical Factor is the reduction factor coming from the finite dimension of magnet blocks."
            ], EditMagnet /* <- id of this cell */
        ],
        [EditPhaseErrConfig, [
            "Open a dialog to configure how to evaluate the phase error.",
            WriteFigure("phaseerr.png", "Dialog for configuration of the phase error evaluation.", false),
            "\"Threshold\" means the normalized peak field of magnet poles, below which they are regarded as those for the end correction section and are neglected for the phase error evaluation."
            ], EditPhaseErrConfig
        ],
        [EditUnitsLabel, [
            "Open a dialog to select the unit of items in the "+GetLink(sections.dataimp, "data file to be imported")+".",
            WriteFigure("unitconf.png", "Dialog to select the unit of items in the data file to be imported.", false),
            "Note that the selection should be made before importing the data. After importing, change of the unit in this dialog has no effect."
            ], EditUnitsLabel
        ],
        [EditAccuracy, [
            "Open a dialog to customize the target numerical accuracy.",
            WriteFigure("accuracy.png", "Dialog to customize the target accuracy.", false),
            "This menu is not available if "+GetQString(DefaultLabel)+" is selected for "+GetLink(ConfigOptionsLabel.accuracy[0], ConfigOptionsLabel.accuracy[0])+" option.",
            "There are a number of parameters to specify the numerical accuracy, according to the numerical method and target item. For example, "+GetQString("Trajectory Step")+" specifies the step size to be used in integration along the longitudinal axis (the larger, the finer). "+GetQString("Discretization")+" specifies the interval of grid points to be used to discretize some target function, which is later used for interpolation. Most of the parameters are specified by an integer, and larger values result in a higher accuracy (and thus a longer CPU time). Note that "+GetQString("Integral Tolereance")+", which specifies the tolerance of the Monte-Carlo integration, should be given by a decimal number. "+GetQString("Maximum Macroparticles")+" is the maximum number of macroparticles to be used in the Monte-Carlo method. If "+GetQString("Limit Macroparticles")+" option is disabled, this parameter is ignored."
            ], EditAccuracy
        ],
        [EditMPIConfig, [
            "Open a dialog to configure the parallel computing.",
            WriteFigure("mpiconf.png", "Dialog for configuration of the parallel computing.", false),
            "Enable Parallel Computing: enable or disable the parallel computing",
            "Number of Processes: number of processes to launch",
            "Note that MPI (message passing interface) environment should be installed for parallel computing, and the path to \"mpiexec\" should be set."
        ], EditMPIConfig]
    ];
    return GetTable(caption, titles, dlgconts);
}

function GetPlotlyDialog()
{
    let caption = "Configurations for the graphical plot";
    let titles = ["Item", "Details"];
    let dlgconts = [
        [PlotOptionsLabel.xscale[0], "Select the scale for x axis (linear/log)."],
        [PlotOptionsLabel.yscale[0], "Select the scale for y axis (linear/log)."],
        [PlotOptionsLabel.type[0], "Select the type of the 1D plot: \"Line\" and/or \"Symbol\"."],
        [PlotOptionsLabel.type2d[0], "Select the type of the 2D plot: \"Contour\" or \"Surface\"."],
        [PlotOptionsLabel.colorscale[0], "Select the color scale. Several built-in options are available but cannot be customized."],
        [PlotOptionsLabel.normalize[0], "Select how to normalize the animation plot. \"For Each\" means that the z-axis scale is normalized by the maximum value for each slide, while \"By Maximum\" means the normalization by the maximum value over the whole slides."]
    ];
    return GetTable(caption, titles, dlgconts);
}

function GetCMDResult()
{
    let caption = "Keys and details of the "+GetQString(CMDResultLabel)+" object";
    let titles = ["Key", "Details", "Symbol", "Unit"];
    let valietms = [
        "",
        MatrixErrLabel+": numerical error in Cholesky expansion", 
        FluxErrLabel+": total amount of the normalized photon flux contained in each coherent mode", 
        WignerErrLabel+": consistency between the original and reconstructed Wigner functions"
    ]
    let validity = WriteListedItem(valietms, false);
    let cmdcont = [
        [MaxOrderLabel, "Maximum order of the Hermite-Gaussian (HG) functions to form the coherent mode", "", ""],
        [WavelengthLabel, "Wavelength of the Wigner function used for CMD ", "$\\lambda$", "m"],
        [FluxCMDLabel, "Total photon flux evaluated from the Wigner function", "$F$", "photons/sec/0.1%b.w."],
        [SrcSizeLabel, "Parameters to define the arguments of HG functions", "$\\sigma$ or $\\sigma_{x,y}$ (1D or 2D)", "m"],
        [OrderLabel, "Indices to define the orders of HG functions for a specific coherent mode", "", ""],
        [CMDErrorLabel, [
            "Validity of the CMD", validity
        ], "", ""],
        [NormFactorLabel, "Coefficient to retrieve the Wigner function from the modal amplitude", "$W_0$", "photons/sec/mm<sup>2</sup>/mrad<sup>2</sup>/0.1%b.w."],
        [AmplitudeReLabel, "Matrix to represent the complex amplitude of HG functions for each coherent mode, real part", "", ""],
        [AmplitudeImLabel, "Imaginary part of the above matrix", "", ""]
    ];
    return GetTable(caption, titles, cmdcont);
}

function GetCMDPostProcess()
{
    let caption = "Objects available by post-processing the CMD results";
    let titles = ["Object Name", "Details"];
    let cmdcont = [
        [CMDModalFluxLabel, "Information about how much flux is contained in each coherent mode."],
        [CMDFieldLabel+"/"+CMDIntensityLabel, "Spatial profile of the complex field amplitude/intensity calculated for each coherent mode. Note that the calculation range and number of points are specified in "+GetLink(CMDParameterLabel, CMDParameterLabel)+"."],
        [CMDCompareIntLabel, "Flux density profile reconstructed from the modal and Wigner functions by projection to the real space (X,Y)"],
        [CMDCompareXLabel, "Wigner function reconstructed from the modal profile, to be compared with the original one to check how the CMD was successful. To facilitate the comparison, both functions are projected on the (X,X') phase space."],
        [CMDCompareYLabel, "Same as the above, but for the (Y,Y') phase space."]
    ];
    return GetTable(caption, titles, cmdcont);
}

function GetFELData()
{
    let caption = "Objects available when "+GetLink(ConfigOptionsLabel.fel[0], ConfigOptionsLabel.fel[0], false)+" option is enabled.";
    let titles = ["Object Name", "Details"];
    let cmdcont = [
        [FELCurrProfile, "Current profile of the electron beam."],
        [FELEtProfile, "Electron density in the E-t (energy-time) phase space."],
        [FELCurrProfileR56, "Current profile of the electron beam after passing through a virtual dispersive section. Available if "+GetLink(ConfigOptionsLabel.R56Bunch[0], ConfigOptionsLabel.R56Bunch[0], false)+" option is enabled."],
        [FELEtProfileR56, "Electron density in the (E-t) phase space after the virtual dispersive section. Available if "+GetLink(ConfigOptionsLabel.R56Bunch[0], ConfigOptionsLabel.R56Bunch[0], false)+" option is enabled."],
        [FELBunchFactor, "Bunch factor of the electron beam."],
        [FELPulseEnergy, "Total energy of the radiation pulse."],
        [FELEfield, "Waveform of the on-axis electric field of radiation in the far-field zone."],
        [FELInstPower, "Temporal profile of the instantaneous radiation power."],
        [FELSpectrum, "Spectrum of the radiation pulse."]
    ];
    return GetTable(caption, titles, cmdcont);
}

function GetWignerRelated()
{
    let caption = "Properties calculated by a mathematical operation of the 4D Wigner Function";
    let titles = ["Property", "Details"];
    let cmdcont = [
        [sections.separa, "In most cases, especially when the electron beam emittance is not too small compared to the optical emittance at the target wavelength, the phase-space density and thus the Wigner function can be separated into two functions $W_x$ and $W_y$. Namely, the Wigner function $W$ can be substituted for by $W_d = W_xW_y/F$, where $F$ is the total photon flux, and the numerical cost for evaluation of the phase-space density is significantly reduced. To evaluate the consistency between the two functions $W$ and $W_d$ and to examine if the above discussions are valid under a specific condition, the separability $\\kappa$ has been introduced, which is defined as \\[\\kappa=1-\\sqrt{\\frac{\\langle(W_d-W)\\rangle^2}{\\langle W^2\\rangle}},\\] where $\\langle f\\rangle$ denotes the average of the function $f$ over the range of interest.", sections.separa],   
        [sections.degcoh, "The degree of spatial coherence $\\zeta$ in SPECTRA is defined as \\[\\zeta=\\left(\\frac{\\lambda}{F}\\right)^2\\int\\!\\!\\!\\!\\int W^2(\\boldsymbol{r},\\boldsymbol{r}')d\\boldsymbol{r}\\boldsymbol{r}',\\] which is actually a spatial average of the degree of spatial coherence $\\mu^2(\\boldsymbol{r}_1,\\boldsymbol{r}_2)$ usually calculated at two different points $\\boldsymbol{r}_1$ and $\\boldsymbol{r}_2$. This is to avoid the complexity of expressing the function by two coordinate variables. Using the two functions $W_x$ and $W_y$, we can also define the degree of spatial coherence in the horizontal or vertical direction in a similar manner.", sections.degcoh]
    ];
    return GetTable(caption, titles, cmdcont);
}

function GetPython()
{
    let caption = "Functions available in the python script.";
    let titles = ["Function", "Arguments", "Details", "Return Format"];
    let funcont = [
        ["Set", "string", "Set the JSON object for the input parameters & options. Return true if OK.", "bool"],
        ["IsReady", "none", "Inquire if the parameters and options are properly set.", "bool"],
        ["Run", "none", "Start the calculation. Returns an exit code upon completion; non-zero values mean that the calculation failed.", "bool"],
        ["GetCaptions", "none", "Returns a dictionary with the keys of \"titles\" & \"units\", and the values (array of strings) indicating the calculated items and their units.", "dict"],
        ["GetData", "none", "Returns a dictionary with the keys of \"variables\" & \"data\". The values of the former and latter mean the independent variable(s) and calculation results.", "dict"],
        ["GetDetailData", "integer", "In some calculations, a key \"details\" is included in the dictionary returned by \"GepCaptions\", meaning that there are a number of data sets, each of which is characterized by the values of the \"details\" key. In such a case, this function should be called instead of the above one, with an argument (integer) to specify the index of the data.", "dict"],
        ["GetCMDCaptions", "string", "Same as GetData but for the CMD results. The argument specifies the key of the data to be retrieved.", "dict"],
        ["GetCMDData", "string", "Same as GetCaptions but for the CMD results. The argument specifies the key of the data to be retrieved.", "dict"],
        ["Test", "none", "Test the library.", "None"]
    ];
    return GetTable(caption, titles, funcont);
}

function GetE1scanList()
{
    let caption = "Relation between K<sub>x</sub> and K<sub>y</sub> in &epsilon;<sub>1st</sub> scan.";
    let titles = [SrcPrmsLabel.gaplink[0], "Details"];
    let funcont = [
        [NoneLabel, "K<sub>x</sub>/K<sub>y</sub> is the same as that currently displayed in the GUI, and is kept constant for different values of &epsilon;<sub>1st</sub>."],
        [AutomaticLabel, "K<sub>x</sub>/K<sub>y</sub> is determined by "+GetQString(SrcPrmsLabel.geofactor[0])+"."],
        [ImpGapTableLabel, "K<sub>x</sub>/K<sub>y</sub> is determined by "+GetQString(SrcPrmsLabel.gaptbl[0])+" data imported in "+GetLink(sections.preproc, sections.preproc)+" subpanel."]
    ];
    return GetTable(caption, titles, funcont);
}

function GetReference(refidx)
{
    let reflists = [
        {
            spectrajsr: "T. Tanaka and H. Kitamura, \"SPECTRA - a synchrotron radiation calculation code,\" J. Synchrotron Radiation 8, 1221 (2001)"
        },
        {
            spectrasri: "T. Tanaka and H. Kitamura, \"Recent Progress of the Synchrotron Radiation Calculation Code SPECTRA\", Proc. 9th Int. Conf. Synchrotron Rad. Instrum. (SRI2006), 355"
        },
        {
            spectra11jsr: "T. Tanaka, \"Major upgrade of the synchrotron radiation calculation code SPECTRA,\" J. Synchrotron Radiation 28, 1267 (2021)"
        },
        {
            refwigner: "T. Tanaka, \"Numerical methods for characterization of synchrotron radiation based on the Wigner function method,\" Phys. Rev. ST-AB 17, 060702 (2014)"
        },
        {
            refcmd: "T. Tanaka, \"Coherent mode decomposition using mixed Wigner functions of Hermite-Gaussian beams,\" Optics Letters 42, 1576 (2017)"
        },
        {
            refsegment: "T. Tanaka and H. Kitamura, \"Simple scheme for harmonic suppression by undulator segmentation,\" Journal of Synchrotron Radiation 9, 266 (2002)"
        },
        {
            refsegx: "T. Tanaka and H. Kitamura, \"Production of linear polarization by segmentation of helical undulator,\" Nucl. Instrum. Meth. A490, 583 (2002)"
        },
        {
            refperr: "R. Walker, \"Interference effects in undulator and wiggler radiation sources\", Nucl. Instrum. Methods Phys. Res., Sect. A 335, 328 (1993)"
        },
        {
            refunivperr: "T. Tanaka, \"Universal representation of undulator phase errors,\" Phys. Rev. AB 21, 110704 (2018)"
        }
    ];
    let refol = document.createElement("ol")
    refol.className = "paren";
    for(let j = 0; j < reflists.length; j++){
        let refi = document.createElement("li");
        let keys = Object.keys(reflists[j]);
        refi.innerHTML = reflists[j][keys[0]];
        refi.id = keys[0];
        refol.appendChild(refi);
        refidx[keys[0]] = "["+(j+1).toString()+"]";
    }
    return refol.outerHTML;
}

function ExportHelpFile()
{
    let prmlabels = [AccPrmsLabel, SrcPrmsLabel, ConfigPrmsLabel];
    let espchars = RetrieveAllEscapeChars(prmlabels);
    espchars.push("&uarr;");

    let baseobj = CopyJSON(help_body);
    let data =
    '<!DOCTYPE html>\n<html lang="en">\n<head>\n<title>Reference Manual for SPECTRA '+Version+'</title>\n'
    +'<link rel="stylesheet" type="text/css" href="reference.css">\n'
    +"<script>MathJax = {chtml: {matchFontHeight: false}, tex: { inlineMath: [['$', '$']] }};</script>\n"
    +'<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>\n'
    +'</head>\n<body>\n'
    +'<div style="display: flex;">\n'
    +'<div class="sidemenu">\n'

    data += GetMenu(baseobj);

    data += '</div>\n<div class="main">';

    let cont = "";
    for(let j = 0; j < baseobj.length; j++){
        cont += WriteObject(0, baseobj[j]);
    }

    let acctbl = GetAccPrmList();
    let srctbl = GetSrcPrmList();
    let srctypetble = GetSrcTypesTable();
    let conftbl = GetConfigPrmList();
    let outfiletbl = GetOutputPrmList();
    let calctype = GetSPECTRAMenuTable(true);

    let pptble = GetPreprocDetailTable();
    let imptbl = GetImportDetailTable();
    let outdatatbl = GetOutDataInf();
    let outitemstbl = GetOutputItems();

    let accjson  =  GetAccPrmTable();
    let srcjson =  GetSrcPrmTable();
    let conjson =  GetConfigPrmTable();
    let outjson =  GetOutFilePrmTable();

    let filemenu = GetFileMenu();
    let runmenu = GetRunMenu();
    let setupdlg = GetSetupDialog();
    let plotlydlg = GetPlotlyDialog();

    let cmdresult = GetCMDResult();
    let cmdpp = GetCMDPostProcess();

    let felvar = GetFELData();

    let wigrel = GetWignerRelated();
    let python = GetPython();

    let e1scanlist = GetE1scanList();

    let contrep = cont 
        .replace("<p>@filemenu</p>", filemenu)
        .replace("<p>@runmenu</p>", runmenu)
        .replace("<p>@setupdlg</p>", setupdlg)
        .replace("<p>@plotlyedit</p>", plotlydlg)
        .replace("<p>@accprm</p>", acctbl)
        .replace("<p>@srcprm</p>", srctbl)
        .replace("<p>@srctype</p>", srctypetble)
        .replace("<p>@confprm</p>", conftbl)
        .replace("<p>@outfile</p>", outfiletbl)
        .replace("<p>@calctype</p>", calctype)
        .replace("<p>@accjson</p>", accjson)
        .replace("<p>@srcjson</p>", srcjson)
        .replace("<p>@confjson</p>", conjson)
        .replace("<p>@outjson</p>", outjson)
        .replace("<p>@preproc</p>", pptble)
        .replace("<p>@import</p>", imptbl)
        .replace("<p>@cmdresult</p>", cmdresult)
        .replace("<p>@cmdpp</p>", cmdpp)
        .replace("<p>@felvar</p>", felvar)
        .replace("<p>@wigrel</p>", wigrel)
        .replace("<p>@python</p>", python)
        .replace("<p>@outitems</p>", outitemstbl)
        .replace("<p>@reference</p>", referencelist)
        .replace("<p>@e1scan</p>", e1scanlist)
        .replace("<p>@outdata</p>", outdatatbl);

    data += FormatHTML(contrep);

    data += "</div>\n</body>\n";
    data = ReplaceSpecialCharacters(espchars, data);

    let blob = new Blob([data], {type:"text/html"});
    let link = document.createElement("a");
    link.href = window.URL.createObjectURL(blob);
    link.download = "reference.html";
    link.click();
    link.remove();
}
