import { Component, Input, OnInit } from '@angular/core';
import { Challenge } from './challenge';

@Component({
  selector: 'app-challenge',
  templateUrl: './challenge.component.html',
  styleUrls: ['./challenge.component.scss'],
})
export class ChallengeComponent  {

  @Input()  challenge!: Challenge 


  constructor() {
  }



  //complete challenge
  destroy(element:PointerEvent):void  {
    let elem = (element.target as HTMLElement)
    elem.parentElement.remove()
    console.log(elem.parentElement)
    //Todo : update server
    this.addPoints(elem)

  }

  addPoints(elem:HTMLElement){
    let classType = elem.className
    console.log("adding x to score",classType)
    //Update user score here
  }



}
