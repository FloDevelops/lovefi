import {
  collection,
  getDocs,
  getDoc,
  addDoc,
  deleteDoc,
  doc,
  query,
  where,
  orderBy,
  limit,
  setDoc,
  collectionGroup,
  Timestamp,
} from "firebase/firestore";
import { firestoreDb } from "./firebase";

// CREATE
export const add = async (colId: string, document: Object) => {
  // @ts-ignore
  const colRef = collection(firestoreDb, colId);
  const docRef = await addDoc(colRef, document);

  return docRef;
};

// READ
// export const queryByCollection = async (colId: string) => {
//   // @ts-ignore
//   const colRef = collection(firestoreDb, colId);
//   const snapshot = await getDocs(colRef);

//   const docs = Array.from(snapshot.docs).map((doc) => {
//     return {
//       ...doc.data(),
//       id: doc.id,
//     };
//   });

//   return docs;
// };

// GET 10 LATEST DOCUMENTS
export const queryXLatest = async (colId: string, count: number) => {
  // @ts-ignore
  const colRef = collection(firestoreDb, colId);
  const q = query(colRef, orderBy("date", "desc"), limit(count));
  const snapshot = await getDocs(q);

  const docs = Array.from(snapshot.docs).map((doc) => {
    return {
      ...doc.data(),
      id: doc.id,
    };
  });

  return docs;
};


// UPDATE
export const update = async (colId: string, document: Object) => {
  await setDoc(doc(collection(firestoreDb, colId)), document, { merge: true });
};

// DELETE
export const del = async (col: string, id: string) => {
  const docRef = doc(firestoreDb, col, id);
  return await deleteDoc(docRef);
};