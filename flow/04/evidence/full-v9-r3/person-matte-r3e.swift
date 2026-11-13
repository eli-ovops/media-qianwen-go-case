import Foundation
import Vision
import CoreImage
import CoreVideo
let w=540,h=960,n=w*h*4
let context=CIContext(options:[.cacheIntermediates:false])
let request=VNGeneratePersonSegmentationRequest();request.qualityLevel = .accurate;request.outputPixelFormat=kCVPixelFormatType_OneComponent8
let faceRequest=VNDetectFaceRectanglesRequest();let handler=VNSequenceRequestHandler()
let input=FileHandle.standardInput,output=FileHandle.standardOutput
func smooth(_ a:Float,_ b:Float,_ x:Float)->Float {let t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)}
var frame=0
while true {
 var data=Data();while data.count<n {let c=input.readData(ofLength:n-data.count);if c.isEmpty{break};data.append(c)};if data.isEmpty{break};if data.count != n{fatalError("partial frame")}
 try autoreleasepool {
 var pb:CVPixelBuffer?;CVPixelBufferCreate(nil,w,h,kCVPixelFormatType_32BGRA,[kCVPixelBufferIOSurfacePropertiesKey:[:] ] as CFDictionary,&pb)
 let pixel=pb!;CVPixelBufferLockBaseAddress(pixel,[]);data.withUnsafeBytes{p in for y in 0..<h{memcpy(CVPixelBufferGetBaseAddress(pixel)!.advanced(by:y*CVPixelBufferGetBytesPerRow(pixel)),p.baseAddress!.advanced(by:y*w*4),w*4)}};CVPixelBufferUnlockBaseAddress(pixel,[])
 try handler.perform([request,faceRequest],on:pixel,orientation:.up)
 guard let obs=request.results?.first,let face=faceRequest.results?.max(by:{$0.boundingBox.width<$1.boundingBox.width}) else{fatalError("missing mask/face")}
 let b=face.boundingBox;let fx=Float(b.minX)*Float(w),fy=Float(1-b.maxY)*Float(h),fw=Float(b.width)*Float(w),fh=Float(b.height)*Float(h)
 var mask=CIImage(cvPixelBuffer:obs.pixelBuffer);mask=mask.transformed(by:CGAffineTransform(scaleX:CGFloat(w)/mask.extent.width,y:CGFloat(h)/mask.extent.height))
 var mb=[UInt8](repeating:0,count:n);context.render(mask,toBitmap:&mb,rowBytes:w*4,bounds:CGRect(x:0,y:0,width:w,height:h),format:.BGRA8,colorSpace:CGColorSpaceCreateDeviceRGB())
 var bytes=[UInt8](data);var alpha=[Float](repeating:0,count:w*h);
 for y in 0..<h{for x in 0..<w{let i=y*w+x,k=i*4;let blue=Float(bytes[k]),green=Float(bytes[k+1]),red=Float(bytes[k+2]),m=Float(mb[k])/255
 var a=smooth(0.77,0.87,m)
 let skin=red>green+10 && green>blue+6 && red>70
 if skin {a=max(a,smooth(0.16,0.42,m))}
 let chairZone=CommandLine.arguments.contains("close") && Float(y)>fy+fh*0.62 && Float(y)<fy+fh*0.86 && Float(x)<fx+fw*0.26
 if chairZone && red<green+25 && blue>red-40 && green>65 {a=0}
 alpha[i]=a
 }}
 // Restore a narrow continuous original-pixel track along the external left lens rim.
 let cy=fy+fh*0.429,cx=fx+fw*0.222,rx=fw*0.175,ry=fh*0.153
 let ya=max(0,Int(fy+fh*0.31)),yb=min(h-1,Int(fy+fh*0.57)),band=19
 var scores=[[Float]](),back=[[Int]](),positions=[[Int]]()
 if yb>ya {for y in ya...yb {
  let dy=(Float(y)-cy)/ry;let expected=cx-rx*sqrt(max(0,1-dy*dy));let left=Int(expected)-9
  var row=[Float](repeating:-100000,count:band),prev=[Int](repeating:0,count:band),xs=[Int]()
  for j in 0..<band {let x=max(0,min(w-1,left+j));xs.append(x);let k=(y*w+x)*4
   let blue=Float(bytes[k]),green=Float(bytes[k+1]),red=Float(bytes[k+2]);let lo=min(red,min(green,blue)),hi=max(red,max(green,blue));let local=lo-1.6*(hi-lo)-Float(abs(j-9))*1.5
   if scores.isEmpty{row[j]=local}else{for pj in 0..<band {let delta=abs(positions.last![pj]-x);if delta>3{continue};let val=scores.last![pj]+local-Float(delta)*12;if val>row[j]{row[j]=val;prev[j]=pj}}}
  };scores.append(row);back.append(prev);positions.append(xs)
 }
 var j=scores.last!.enumerated().max(by:{$0.element<$1.element})!.offset
 for r in stride(from:scores.count-1,through:0,by:-1) {let y=ya+r,x=positions[r][j]
  for xx in max(0,x-1)...min(w-1,x+1) {let i=y*w+xx,k=i*4;let lo=min(bytes[k],min(bytes[k+1],bytes[k+2]));if lo>65 && mb[k]>28{alpha[i]=1}}
  j=back[r][j]
 }
 }
 // Remove isolated matte fragments below the glasses. Never remove the connected hand/body.
 var visited=[Bool](repeating:false,count:w*h)
 let cutoff=Int(fy+fh*0.60)
 for first in 0..<(w*h) {
  if visited[first] || alpha[first]<0.12{continue}
  var group=[first],cursor=0;visited[first]=true
  while cursor<group.count {let i=group[cursor];cursor+=1;let x=i%w
   for j in [i-w,i+w,x>0 ? i-1 : -1,x<w-1 ? i+1 : -1] {if j>=0 && j<w*h && !visited[j] && alpha[j]>=0.12{visited[j]=true;group.append(j)}}
  }
  if group.count<80 && group.allSatisfy({$0/w>cutoff}) {for i in group{alpha[i]=0}}
 }
 for i in 0..<(w*h){let k=i*4,a=alpha[i];for c in 0..<3{let bg:Float=c==0 ? 17 : (c==1 ? 13 : 9);bytes[k+c]=UInt8(max(0,min(255,Float(bytes[k+c])*a+bg*(1-a))))};bytes[k+3]=255}
 output.write(Data(bytes))
 };frame+=1;if frame%120==0{FileHandle.standardError.write(Data("MATTE \(frame)\n".utf8))}
}
FileHandle.standardError.write(Data("COMPLETE \(frame)\n".utf8))
