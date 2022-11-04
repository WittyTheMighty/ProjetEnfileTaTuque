import { Component } from '@angular/core';


@Component({
  selector: 'app-tab2',
  templateUrl: 'tab2.page.html',
  styleUrls: ['tab2.page.scss'],
})
export class Tab2Page  {

  private challenges:any

              
 


  constructor() {}

  ionViewWillEnter() {
    console.log("ionViewWillEnter")
    this.challenges = [{title:"Défi: Enfile ta tuque",
    timeStart:"7h00",
    timeEnd:"10h00",
    description:"Baisser votre chauffage de deux degrés. Le chauffage est la principale source de consommation l'hiver"
    },
    {title:"Défi: Chasses aux chargeurs fantomes",
    timeStart:"18h",
    timeEnd:"19h30",
    description:"Certains chargeurs peuvent consommer de l'énergie même si aucun appareil est branché."
    },
    {title:"Défi: Ferme les lumières!",
    timeStart:"9h",
    timeEnd:"11h",
    description:"Ferme les lumières"
    }
  ]
  }






  // createChallengeCardComponent(){
  //   let childList = (this.el.nativeElement as HTMLElement).childNodes
  //   console.log(childList)
  //   let challengeContainer 
  //   childList.forEach(element => {
  //     console.log()
  //     if ((element as HTMLElement).id == "challengeContent"){
  //       console.log("inside if stament")
  //       challengeContainer = element
  //     }
      
  //   });
    
  //   console.log("challenge Container:", challengeContainer.childNodes[0])
  //   let component = this.viewContainerRef.createComponent(ChallengeComponent);

  // }

}
