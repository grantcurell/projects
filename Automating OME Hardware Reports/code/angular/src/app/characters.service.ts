import { Injectable } from '@angular/core';
import { Character } from './character'
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { DomSanitizer } from '@angular/platform-browser';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CharactersService {

  private api_ip = 'http://192.168.1.6:5000';
  private lookup_url = this.api_ip +  '/api/lookup';
  public charactersBehaviorSubject = new BehaviorSubject<Character[]>([]);
  public charactersSearchError: string;

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  getChar(characters_to_lookup: string): void {
    this.http.put<Character[]>(this.lookup_url, {"characters_to_lookup": characters_to_lookup}, this.httpOptions).pipe(
      map(characters => {

        for (const [i,character] of characters.entries()) {
          if (character.images !== undefined && character.images.length > 0) {
            // Right now we are assuming that there is only one image
            let objectURL = 'data:image/jpeg;base64,' + character.images[0][1];
            characters[i].thumbnail = this.sanitizer.bypassSecurityTrustUrl(objectURL);
          } else {
            characters[i].thumbnail = undefined;
          }
        }

        return characters;
      })
    ).subscribe(
      {
        next: x => {
          this.charactersBehaviorSubject.next(x);
          this.charactersSearchError = undefined;
        },
        error: err => {
          console.error('We received an error while retrieving the character: ' + err);
          this.charactersSearchError = "We were unable to find the character you were looking for.";
          this.charactersBehaviorSubject.next([]);
        },
        complete: () => {
          console.log('Received the character form the API server successfully!');
        },
      }
    )
  }

  constructor(private http: HttpClient, private sanitizer: DomSanitizer) { }
}
