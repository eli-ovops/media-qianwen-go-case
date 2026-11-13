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
 var bytes=[UInt8](data);var alpha=[Float](repeating:0,count:w*h);var candidates=[Bool](repeating:false,count:w*h);var queue=[Int]()
 for y in 0..<h{for x in 0..<w{let i=y*w+x,k=i*4;let blue=Float(bytes[k]),green=Float(bytes[k+1]),red=Float(bytes[k+2]),m=Float(mb[k])/255
 var a=smooth(0.77,0.87,m)
 let skin=red>green+10 && green>blue+6 && red>70
 if skin {a=max(a,smooth(0.16,0.42,m))}
 let eyeZone=Float(y)>fy+fh*0.20 && Float(y)<fy+fh*0.61
 let silver=min(red,min(green,blue))>75 && max(red,max(green,blue))-min(red,min(green,blue))<45
 let dx=(Float(x)-(fx+fw*0.222))/(fw*0.175),dy=(Float(y)-(fy+fh*0.429))/(fh*0.153)
 let ring=abs(sqrt(dx*dx+dy*dy)-1)<0.055
 let externalLens=Float(y)>fy+fh*0.31 && Float(y)<fy+fh*0.60 && Float(x)<fx+fw*0.13
 if externalLens && !skin {a = ring && m>0.18 ? 1 : 0}
 if eyeZone && silver && m>0.18 && !externalLens {candidates[i]=true;if a>0.85 || (externalLens && ring){queue.append(i)}}
 let chairZone=Float(y)>fy+fh*0.62 && Float(y)<fy+fh*0.99 && (Float(x)<fx+fw*0.26 || Float(x)>fx+fw*0.96)
 if chairZone && red<green+25 && blue>red-40 && green>65 {a=0}
 alpha[i]=a
 }}
 var seen=[Bool](repeating:false,count:w*h),cursor=0
 while cursor<queue.count {let i=queue[cursor];cursor+=1;if seen[i]{continue};seen[i]=true;alpha[i]=max(alpha[i],smooth(0.18,0.35,Float(mb[i*4])/255));for d in [-w,w,-1,1] {let j=i+d;if j>=0 && j<w*h && !seen[j] && candidates[j]{queue.append(j)}}}
 for i in 0..<(w*h){let k=i*4,a=alpha[i];for c in 0..<3{let bg:Float=c==0 ? 17 : (c==1 ? 13 : 9);bytes[k+c]=UInt8(max(0,min(255,Float(bytes[k+c])*a+bg*(1-a))))};bytes[k+3]=255}
 output.write(Data(bytes))
 };frame+=1;if frame%120==0{FileHandle.standardError.write(Data("MATTE \(frame)\n".utf8))}
}
FileHandle.standardError.write(Data("COMPLETE \(frame)\n".utf8))
