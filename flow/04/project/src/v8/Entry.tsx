import React from 'react';
import {Composition,registerRoot,staticFile} from 'remotion';
import {loadFont} from '@remotion/fonts';
import {CostReminder} from './CostReminder';
for(const [name,weight] of [['Medium','500'],['Semibold','600'],['Heavy','900']])loadFont({family:'Eli MiSans',url:staticFile(`v8/MiSans-${name}.otf`),weight,format:'opentype'});
registerRoot(()=> <><Composition id="QianwenSampleV8" component={CostReminder} width={1080} height={1920} fps={60} durationInFrames={816}/><Composition id="QianwenSampleV8Cover" component={CostReminder} width={1080} height={1920} fps={60} durationInFrames={816}/></>);
