import React from 'react';
import {Composition,registerRoot,staticFile} from 'remotion';
import {loadFont} from '@remotion/fonts';
import {FullFilm} from './Film';
loadFont({family:'Eli MiSans',url:staticFile('v8/MiSans-Medium.otf'),weight:'500'});
loadFont({family:'Eli MiSans',url:staticFile('v8/MiSans-Semibold.otf'),weight:'600'});
loadFont({family:'Eli MiSans',url:staticFile('v8/MiSans-Heavy.otf'),weight:'900'});
registerRoot(()=> <Composition id="QianwenFullV9" component={FullFilm} width={1080} height={1920} fps={60} durationInFrames={6122}/>);
