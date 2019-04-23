package Project;

import java.util.concurrent.TimeUnit;
import org.junit.*;
import static org.junit.Assert.*;

import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.Select;
import java.util.Random;


public class Room_Add_Failed {
  private WebDriver driver;
  private StringBuffer verificationErrors = new StringBuffer();
  boolean result;
 
  public String random_fuzzer() {
	  Random random = new Random();
	  StringBuilder builder = new StringBuilder();
	  int length = random.nextInt(99)+1;
	  for(int i = 0; i<length;i++) {
		  int n = random.nextInt(94)+33;
		  char s;
		  s=(char) n;
		  System.out.println(s);
		  builder.append(s);
		  
	  }
	  return builder.toString();
  }
  
 
  private String closeAlertAndGetItsText() {
	   boolean acceptNextAlert = true;
	    try {
	      Alert alert = driver.switchTo().alert();
	      String alertText = alert.getText();
	      if (acceptNextAlert) {
	        alert.accept();
	      } else {
	        alert.dismiss();
	      }
	      return alertText;
	    } finally {
	      acceptNextAlert = true;
	    }
	  }
  
  @Before
  public void setUp() throws Exception {
    driver = new FirefoxDriver();
    driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
  }

  @Test
  public void Room_Add_Test() throws Exception {
	String user = "tom";
	String pwd= "sutd1234";
    driver.get("http://127.0.0.1:5000");
    driver.findElement(By.name("username")).click();
    driver.findElement(By.name("username")).clear();
    driver.findElement(By.name("username")).sendKeys(user);
    assertEquals ("tom", user);
    driver.findElement(By.name("pd")).clear();
    driver.findElement(By.name("pd")).sendKeys(pwd);
    assertEquals ("sutd1234", pwd);
    driver.findElement(By.name("pd")).sendKeys(Keys.ENTER);
    
    Thread.sleep(3000);
    String room = random_fuzzer();
    String type = "lt";
    driver.get("http://127.0.0.1:5000/room");
    driver.findElement(By.name("roomName")).click();
    driver.findElement(By.name("roomName")).clear();
    driver.findElement(By.name("roomName")).sendKeys(room);
    new Select(driver.findElement(By.name("roomType"))).selectByVisibleText(type);
    driver.findElement(By.name("add")).click();
    assertEquals("This is a invalid format.", closeAlertAndGetItsText());
    Thread.sleep(7000);
    driver.findElement(By.name("roomName")).clear();
    Thread.sleep(2000);
    java.util.List<WebElement> links = driver.findElements(By.className("table_view_room"));
    System.out.println(links.size());
    String text1;
    
    for(int i =0;i<links.size();i++) {
    	System.out.println(i + " " + links.get(i).getText());
    	text1 = links.get(i).getText();
    	if(room.contentEquals(text1)) {
    		result=true;
    	}
    	
    }
   
    Thread.sleep(5000);
    assertTrue(result);
    assertEquals ("room", driver.getTitle());
  }

  @After
  public void tearDown() throws Exception {
    driver.quit();
    String verificationErrorString = verificationErrors.toString();
    if (!"".equals(verificationErrorString)) {
      fail(verificationErrorString);
    }
  }

}
