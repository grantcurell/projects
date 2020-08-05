import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, FormControl, FormGroupDirective, NgForm, Validators } from '@angular/forms';
import { ErrorStateMatcher } from '@angular/material/core';
import { Character } from '../character';
import { CharactersService } from '../characters.service';



/** Error when invalid control is dirty, touched, or submitted. */
export class MyErrorStateMatcher implements ErrorStateMatcher {
  isErrorState(control: FormControl | null, form: FormGroupDirective | NgForm | null): boolean {
    const isSubmitted = form && form.submitted;
    return !!(control && control.invalid && (control.dirty || control.touched || isSubmitted));
  }
}

@Component({
  selector: 'app-charsearch',
  templateUrl: './charsearch.component.html',
  styleUrls: ['./charsearch.component.css']
})
export class CharsearchComponent implements OnInit {

  characters: Character[];
  characterInput: FormControl;
  characterForm: FormGroup;
  error: string;

  charFormControl = new FormControl('', [
    Validators.required
  ]);

  matcher = new MyErrorStateMatcher();

  constructor(public charactersService: CharactersService, private formBuilder: FormBuilder) {}

  ngOnInit(): void {
    this.characterForm = new FormGroup({
      characterInput: this.formBuilder.control({value: "", disabled: false})
    });
  }

  onSubmit() {
    this.charactersService.getChar(this.characterForm.get("characterInput").value);
  }

}